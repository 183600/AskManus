"""Interactive tool that lets the agent ask the user to choose among options."""

import asyncio
import json
import select
import sys
import threading
from typing import Any, Callable, List, Optional, Tuple

from app.tool.base import BaseTool, ToolResult


_ASK_USER_DESCRIPTION = """Ask the user a question and let them pick from a list of options.
Use this when a decision depends on the user's preference, intent, or on information only the user has, instead of guessing.
Each option may include a short explanation shown to the user, and the user can also type a custom answer unless allow_custom is false."""


class AskUser(BaseTool):
    """Present the user with a question and a set of options to choose from."""

    name: str = "ask_user"
    description: str = _ASK_USER_DESCRIPTION
    parameters: dict = {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question to ask the user.",
            },
            "options": {
                "type": "array",
                "minItems": 1,
                "description": "The options the user can choose from.",
                "items": {
                    "type": "object",
                    "properties": {
                        "label": {
                            "type": "string",
                            "description": "Short name of the option.",
                        },
                        "description": {
                            "type": "string",
                            "description": "Optional explanation shown next to the option.",
                        },
                    },
                    "required": ["label"],
                },
            },
            "allow_custom": {
                "type": "boolean",
                "description": "Whether the user may answer with free-form text instead of picking an option. Default is true.",
                "default": True,
            },
        },
        "required": ["question", "options"],
    }

    max_attempts: int = 3

    async def execute(
        self,
        question: str = "",
        options: Optional[List[Any]] = None,
        allow_custom: bool = True,
        **kwargs: Any,
    ) -> ToolResult:
        """Ask the user to choose an option and return their answer to the agent."""
        question_text = str(question).strip() if question else ""
        if not question_text:
            return ToolResult(error="Parameter `question` is required for ask_user.")

        normalized = self._normalize_options(options)
        if not normalized:
            return ToolResult(
                error="Parameter `options` must contain at least one option for ask_user."
            )

        rendered = self._render(question_text, normalized, allow_custom)

        if not self._stdin_available():
            print(rendered, flush=True)
            labels = ", ".join(
                f"{i}) {label}" for i, (label, _) in enumerate(normalized, 1)
            )
            return ToolResult(
                error=(
                    "No interactive terminal is available, so the user could not answer. "
                    f"Proceed using your best judgment. Question: {question_text} "
                    f"Options: {labels}."
                )
            )

        hint = (
            f"Select 1-{len(normalized)}"
            + (" or type your own answer" if allow_custom else "")
            + ": "
        )
        print(rendered, flush=True)
        for attempt in range(self.max_attempts):
            answer = await self._read_line(hint)
            if answer is None:
                return ToolResult(
                    error=(
                        "The user did not provide an answer (input stream closed). "
                        "Proceed using your best judgment."
                    )
                )

            answer = answer.strip()
            selected = self._match_option(answer, normalized)
            if selected is not None:
                index, (label, description) = selected
                output = f"User selected option {index}: {label}"
                if description:
                    output += f" - {description}"
                return ToolResult(output=output)

            # Numeric answers are treated as option numbers, so an out-of-range
            # number is a mistake rather than a custom answer.
            if allow_custom and answer and not answer.isdigit():
                return ToolResult(output=f"User answered: {answer}")

            if attempt < self.max_attempts - 1:
                print(
                    f"Invalid choice: {answer!r}. Please enter a number between "
                    f"1 and {len(normalized)}"
                    + (" or a custom answer." if allow_custom else "."),
                    flush=True,
                )

        return ToolResult(
            error=(
                f"The user did not provide a valid choice after {self.max_attempts} attempts. "
                "Proceed using your best judgment."
            )
        )

    @staticmethod
    def _normalize_options(options: Optional[List[Any]]) -> List[Tuple[str, str]]:
        """Normalize options to a list of (label, description) tuples."""
        if isinstance(options, str):
            try:
                options = json.loads(options)
            except (TypeError, ValueError):
                options = [options]

        normalized: List[Tuple[str, str]] = []
        for option in options or []:
            if isinstance(option, dict):
                label = str(option.get("label") or option.get("name") or "").strip()
                description = str(option.get("description") or "").strip()
            else:
                label, description = str(option).strip(), ""
            if label:
                normalized.append((label, description))
        return normalized

    @staticmethod
    def _render(
        question: str, options: List[Tuple[str, str]], allow_custom: bool
    ) -> str:
        """Build the text shown to the user before reading their answer."""
        lines = [f"Question: {question}", ""]
        for i, (label, description) in enumerate(options, 1):
            suffix = f" - {description}" if description else ""
            lines.append(f"  {i}) {label}{suffix}")
        if allow_custom:
            lines.append("  (or type your own answer)")
        return "\n".join(lines)

    @staticmethod
    def _match_option(
        answer: str, options: List[Tuple[str, str]]
    ) -> Optional[Tuple[int, Tuple[str, str]]]:
        """Match an answer against the numbered options or their labels."""
        if not answer:
            return None

        if answer.isdigit():
            index = int(answer)
            if 1 <= index <= len(options):
                return index, options[index - 1]

        lowered = answer.lower()
        for index, option in enumerate(options, 1):
            if option[0].lower() == lowered:
                return index, option
        return None

    @staticmethod
    def _stdin_available() -> bool:
        try:
            return sys.stdin is not None and sys.stdin.readable()
        except Exception:
            return False

    @staticmethod
    def _stdin_ready(stdin) -> bool:
        if sys.platform.startswith("win"):
            return False
        try:
            ready, _, _ = select.select([stdin], [], [], 0)
            return bool(ready)
        except Exception:
            return False

    async def _read_line(self, prompt_text: str) -> Optional[str]:
        """Read one line from stdin, or return None when none can be read."""
        stdin = sys.stdin
        if stdin is None:
            return None

        def _read_input() -> str:
            return input(prompt_text)

        def _read_pipe() -> str:
            line = stdin.readline()
            if line == "":
                raise EOFError
            return line

        try:
            if stdin.isatty():
                return await self._threaded_read(_read_input)
            if not self._stdin_ready(stdin):
                return None
            print(prompt_text, flush=True)
            return await self._threaded_read(_read_pipe)
        except Exception:
            return None

    @staticmethod
    async def _threaded_read(read_func: Callable[[], str]) -> Optional[str]:
        """Run a blocking read in a daemon thread.

        A daemon thread keeps ``Ctrl+C`` from deadlocking the process while
        the agent waits for the user's answer.
        """
        loop = asyncio.get_running_loop()
        future: asyncio.Future = loop.create_future()

        def _deliver(result: Optional[str]) -> None:
            if not future.done():
                future.set_result(result)

        def _worker() -> None:
            try:
                # An empty string is a blank answer (invalid input), only
                # EOF maps to None ("stream closed").
                result: Optional[str] = read_func()
            except (EOFError, OSError):
                result = None
            except Exception:
                result = None
            try:
                loop.call_soon_threadsafe(_deliver, result)
            except RuntimeError:
                pass

        threading.Thread(target=_worker, daemon=True).start()
        return await future


if __name__ == "__main__":
    result = asyncio.run(
        AskUser().execute(
            question="Which database should I use?",
            options=[
                {"label": "SQLite", "description": "simple, file based"},
                {"label": "PostgreSQL", "description": "production ready"},
            ],
        )
    )
    print(result)
