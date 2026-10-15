"""
Asynchronous Docker Terminal

This module provides asynchronous terminal functionality for Docker containers,
allowing interactive command execution with timeout control.
"""

import asyncio
import re
import socket
from typing import Dict, Optional, Tuple, Union

import docker
from docker import APIClient
from docker.errors import APIError
from docker.models.containers import Container


class DockerSession:
    def __init__(self, container_id: str, api: Optional[APIClient] = None) -> None:
        """Initializes a Docker session.

        Args:
            container_id: ID of the Docker container.
            api: Optional existing Docker API client to reuse instead of
                creating a new connection pool.
        """
        self.api = api if api is not None else APIClient()
        self.container_id = container_id
        self.exec_id = None
        self.socket = None

    async def create(self, working_dir: str, env_vars: Dict[str, str]) -> None:
        """Creates an interactive session with the container.

        Args:
            working_dir: Working directory inside the container.
            env_vars: Environment variables to set.

        Raises:
            RuntimeError: If socket connection fails.
        """
        startup_command = [
            "bash",
            "-c",
            f"cd {working_dir} && "
            "PROMPT_COMMAND='' "
            "PS1='$ ' "
            "exec bash --norc --noprofile",
        ]

        exec_data = await asyncio.to_thread(
            self.api.exec_create,
            self.container_id,
            startup_command,
            stdin=True,
            tty=True,
            stdout=True,
            stderr=True,
            privileged=True,
            user="root",
            environment={**env_vars, "TERM": "dumb", "PS1": "$ ", "PROMPT_COMMAND": ""},
        )
        self.exec_id = exec_data["Id"]

        socket_data = await asyncio.to_thread(
            self.api.exec_start,
            self.exec_id,
            socket=True,
            tty=True,
            stream=True,
            demux=True,
        )

        if hasattr(socket_data, "_sock"):
            self.socket = socket_data._sock
            self.socket.setblocking(False)
        else:
            raise RuntimeError("Failed to get socket connection")

        await self._read_until_prompt()

    async def close(self) -> None:
        """Cleans up session resources.

        1. Sends exit command
        2. Closes socket connection
        3. Checks and cleans up exec instance
        """
        try:
            if self.socket:
                # Send exit command to close bash session
                try:
                    self.socket.sendall(b"exit\n")
                    # Allow time for command execution
                    await asyncio.sleep(0.1)
                except:
                    pass  # Ignore sending errors, continue cleanup

                # Close socket connection
                try:
                    self.socket.shutdown(socket.SHUT_RDWR)
                except:
                    pass  # Some platforms may not support shutdown

                self.socket.close()
                self.socket = None

            if self.exec_id:
                try:
                    # Wait (bounded) until the exec instance stops running
                    # instead of sleeping a fixed amount of time.
                    loop = asyncio.get_running_loop()
                    deadline = loop.time() + 1.0
                    while loop.time() < deadline:
                        exec_inspect = await asyncio.to_thread(
                            self.api.exec_inspect, self.exec_id
                        )
                        if not exec_inspect.get("Running", False):
                            break
                        await asyncio.sleep(0.05)
                except:
                    pass  # Ignore inspection errors, continue cleanup

                self.exec_id = None

        except Exception as e:
            # Log error but don't raise, ensure cleanup continues
            print(f"Warning: Error during session cleanup: {e}")

    async def _read_until_prompt(self) -> str:
        """Reads output until prompt is found.

        Returns:
            String containing output up to the prompt.

        Raises:
            socket.error: If socket communication fails.
        """
        loop = asyncio.get_running_loop()
        marker = b"$ "
        buffer = bytearray()
        while True:
            chunk = await loop.sock_recv(self.socket, 4096)
            if not chunk:
                break
            # Only search the newly received bytes plus one byte of overlap,
            # so repeated scans stay linear in the total output size.
            search_from = max(0, len(buffer) - (len(marker) - 1))
            buffer.extend(chunk)
            if buffer.find(marker, search_from) != -1:
                break
        return buffer.decode("utf-8")

    async def execute(self, command: str, timeout: Optional[int] = None) -> str:
        """Executes a command and returns cleaned output.

        Args:
            command: Shell command to execute.
            timeout: Maximum execution time in seconds.

        Returns:
            Command output as string with prompt markers removed.

        Raises:
            RuntimeError: If session not initialized or execution fails.
            TimeoutError: If command execution exceeds timeout.
        """
        if not self.socket:
            raise RuntimeError("Session not initialized")

        try:
            # Sanitize command to prevent shell injection
            sanitized_command = self._sanitize_command(command)
            full_command = f"{sanitized_command}\necho $?\n"
            loop = asyncio.get_running_loop()
            await loop.sock_sendall(self.socket, full_command.encode())

            async def read_output() -> str:
                buffer = bytearray()
                result_lines = []
                command_sent = False
                exit_echo_seen = False
                exit_code_seen = False
                idle_timeout = 0.1

                def process(chunk: bytes) -> None:
                    nonlocal buffer, command_sent, exit_echo_seen, exit_code_seen
                    buffer.extend(chunk)

                    # Consume only complete lines, scanning just the newly
                    # received bytes instead of re-splitting the whole buffer.
                    start = 0
                    while True:
                        newline = buffer.find(b"\n", start)
                        if newline == -1:
                            break
                        line = bytes(buffer[start:newline]).rstrip(b"\r")
                        start = newline + 1
                        stripped = line.strip()

                        if not command_sent:
                            command_sent = True
                            continue

                        if stripped in (b"echo $?", b"$ echo $?"):
                            exit_echo_seen = True
                            continue

                        if not exit_echo_seen and stripped.endswith(b"$ echo $?"):
                            exit_echo_seen = True

                        if exit_echo_seen and stripped.isdigit():
                            exit_code_seen = True
                            continue

                        if stripped:
                            result_lines.append(line)

                    if start:
                        del buffer[:start]

                while True:
                    chunk = await loop.sock_recv(self.socket, 4096)
                    if not chunk:
                        break
                    process(chunk)

                    done = False
                    while buffer.endswith(b"$ "):
                        if exit_code_seen:
                            done = True
                            break
                        try:
                            chunk = await asyncio.wait_for(
                                loop.sock_recv(self.socket, 4096), idle_timeout
                            )
                        except asyncio.TimeoutError:
                            done = True
                            break
                        if not chunk:
                            done = True
                            break
                        process(chunk)
                    if done:
                        break

                output = b"\n".join(result_lines).decode("utf-8")
                output = re.sub(r"\n\$ echo \$\$?.*$", "", output)

                return output

            if timeout:
                result = await asyncio.wait_for(read_output(), timeout)
            else:
                result = await read_output()

            return result.strip()

        except asyncio.TimeoutError:
            raise TimeoutError(f"Command execution timed out after {timeout} seconds")
        except Exception as e:
            raise RuntimeError(f"Failed to execute command: {e}")

    def _sanitize_command(self, command: str) -> str:
        """Sanitizes the command string to prevent shell injection.

        Args:
            command: Raw command string.

        Returns:
            Sanitized command string.

        Raises:
            ValueError: If command contains potentially dangerous patterns.
        """

        # Additional checks for specific risky commands
        risky_commands = [
            "rm -rf /",
            "rm -rf /*",
            "mkfs",
            "dd if=/dev/zero",
            ":(){:|:&};:",
            "chmod -R 777 /",
            "chown -R",
        ]

        for risky in risky_commands:
            if risky in command.lower():
                raise ValueError(
                    f"Command contains potentially dangerous operation: {risky}"
                )

        return command


class AsyncDockerizedTerminal:
    def __init__(
        self,
        container: Union[str, Container],
        working_dir: str = "/workspace",
        env_vars: Optional[Dict[str, str]] = None,
        default_timeout: int = 60,
    ) -> None:
        """Initializes an asynchronous terminal for Docker containers.

        Args:
            container: Docker container ID or Container object.
            working_dir: Working directory inside the container.
            env_vars: Environment variables to set.
            default_timeout: Default command execution timeout in seconds.
        """
        self._client = None
        self.container = (
            container
            if isinstance(container, Container)
            else self.client.containers.get(container)
        )
        self.working_dir = working_dir
        self.env_vars = env_vars or {}
        self.default_timeout = default_timeout
        self.session = None

    @property
    def client(self) -> docker.DockerClient:
        """Docker client, created lazily only when it is actually needed."""
        if self._client is None:
            self._client = docker.from_env()
        return self._client

    async def init(self) -> None:
        """Initializes the terminal environment.

        Ensures working directory exists and creates an interactive session.

        Raises:
            RuntimeError: If initialization fails.
        """
        await self._ensure_workdir()

        # Reuse the API client that owns this container when available so we
        # don't open an additional connection pool for the session.
        container_client = getattr(self.container, "client", None)
        api = container_client.api if container_client is not None else None
        self.session = DockerSession(self.container.id, api)
        await self.session.create(self.working_dir, self.env_vars)

    async def _ensure_workdir(self) -> None:
        """Ensures working directory exists in container.

        Raises:
            RuntimeError: If directory creation fails.
        """
        try:
            await self._exec_simple(f"mkdir -p {self.working_dir}")
        except APIError as e:
            raise RuntimeError(f"Failed to create working directory: {e}")

    async def _exec_simple(self, cmd: str) -> Tuple[int, str]:
        """Executes a simple command using Docker's exec_run.

        Args:
            cmd: Command to execute.

        Returns:
            Tuple of (exit_code, output).
        """
        result = await asyncio.to_thread(
            self.container.exec_run, cmd, environment=self.env_vars
        )
        return result.exit_code, result.output.decode("utf-8")

    async def run_command(self, cmd: str, timeout: Optional[int] = None) -> str:
        """Runs a command in the container with timeout.

        Args:
            cmd: Shell command to execute.
            timeout: Maximum execution time in seconds.

        Returns:
            Command output as string.

        Raises:
            RuntimeError: If terminal not initialized.
        """
        if not self.session:
            raise RuntimeError("Terminal not initialized")

        return await self.session.execute(cmd, timeout=timeout or self.default_timeout)

    async def close(self) -> None:
        """Closes the terminal session."""
        if self.session:
            await self.session.close()

    async def __aenter__(self) -> "AsyncDockerizedTerminal":
        """Async context manager entry."""
        await self.init()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.close()
