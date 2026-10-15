import multiprocessing
import queue as _queue
import sys
import time
from io import StringIO
from typing import Dict

from app.tool.base import BaseTool


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

        # Drain the queue while the child runs so that large results can be
        # transferred through the pipe without blocking the child forever.
        result = None
        deadline = time.monotonic() + timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            if not proc.is_alive():
                break
            if result is not None:
                # Result received; give the child the rest of the deadline
                # to shut down cleanly.
                proc.join(remaining)
                break
            try:
                result = result_queue.get(timeout=min(0.1, remaining))
            except _queue.Empty:
                continue

        # timeout process
        if proc.is_alive():
            proc.terminate()
            proc.join(1)
            return {
                "observation": f"Execution timeout after {timeout} seconds",
                "success": False,
            }
        proc.join()

        if result is None:
            # The child flushed the queue right before exiting; collect it now.
            try:
                result = result_queue.get(timeout=1)
            except _queue.Empty:
                result = {"observation": "", "success": False}
        return result
