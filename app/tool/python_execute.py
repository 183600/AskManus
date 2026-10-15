import asyncio
import multiprocessing
import queue as _queue
import sys
import time
from io import StringIO
from typing import Dict, Optional

from app.tool.base import BaseTool


def _get_result(result_queue: multiprocessing.Queue, timeout: float) -> Optional[Dict]:
    """Fetch the child's result, returning None when none arrives in time."""
    try:
        return result_queue.get(timeout=timeout)
    except _queue.Empty:
        return None


class PythonExecute(BaseTool):
    """A tool for executing Python code with timeout and safety restrictions."""

    name: str = "python_execute"
    description: str = "Executes Python code string. Note: Only print outputs are visible, function return values are not captured. Use print statements to see results."
    parameters: dict = {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "The Python code to execute.",
            },
        },
        "required": ["code"],
    }

    def _run_code(
        self, code: str, result_queue: multiprocessing.Queue, safe_globals: dict
    ) -> None:
        original_stdout = sys.stdout
        result = {"observation": "", "success": False}
        try:
            output_buffer = StringIO()
            sys.stdout = output_buffer
            exec(code, safe_globals, safe_globals)
            result["observation"] = output_buffer.getvalue()
            result["success"] = True
        except Exception as e:
            result["observation"] = str(e)
            result["success"] = False
        finally:
            sys.stdout = original_stdout
            result_queue.put(result)
            result_queue.close()
            result_queue.join_thread()

    async def execute(
        self,
        code: str,
        timeout: int = 5,
    ) -> Dict:
        """
        Executes the provided Python code with a timeout.

        Args:
            code (str): The Python code to execute.
            timeout (int): Execution timeout in seconds.

        Returns:
            Dict: Contains 'output' with execution output or error message and 'success' status.
        """

        result_queue: multiprocessing.Queue = multiprocessing.Queue()
        if isinstance(__builtins__, dict):
            safe_globals = {"__builtins__": __builtins__}
        else:
            safe_globals = {"__builtins__": __builtins__.__dict__.copy()}
        proc = multiprocessing.Process(
            target=self._run_code, args=(code, result_queue, safe_globals)
        )
        proc.start()

        def _wait_for_result() -> Optional[Dict]:
            """Collect the child's result without blocking the event loop."""
            result = None
            deadline = time.monotonic() + timeout
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    break
                if not proc.is_alive():
                    break
                if result is not None:
                    proc.join(remaining)
                    break
                try:
                    result = result_queue.get(timeout=min(0.1, remaining))
                except _queue.Empty:
                    continue
            return result

        result = await asyncio.to_thread(_wait_for_result)

        # timeout process
        if proc.is_alive():
            if result is None:
                proc.terminate()
                await asyncio.to_thread(proc.join, 1)
                return {
                    "observation": f"Execution timeout after {timeout} seconds",
                    "success": False,
                }
            # The result was already published; stop the lingering shutdown.
            proc.terminate()
            await asyncio.to_thread(proc.join, 1)
        else:
            proc.join()

        if result is None:
            result = await asyncio.to_thread(_get_result, result_queue, 1)
            if result is None:
                result = {"observation": "", "success": False}
        return result
