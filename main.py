import asyncio
import sys

from app.agent.manus import Manus
from app.logger import logger


_QUIT_COMMANDS = {"exit", "quit", "q"}


async def _handle_request(agent: Manus, prompt: str) -> None:
    logger.warning("Processing your request...")
    await agent.run(prompt)
    logger.info("Request processing completed.")


async def main():
    agent = Manus()
    try:
        prompt = input("Enter your prompt: ")
        if not prompt.strip():
            logger.warning("Empty prompt provided.")
            return

        await _handle_request(agent, prompt)

        interactive = sys.stdin is not None and sys.stdin.isatty()
        if interactive:
            logger.info("Session started. Enter 'exit' to quit.")

        while interactive:
            try:
                follow_up = input("\nEnter your prompt (or 'exit' to quit): ")
            except EOFError:
                break

            if follow_up.strip().lower() in _QUIT_COMMANDS:
                break
            if not follow_up.strip():
                logger.warning("Empty prompt provided.")
                continue

            try:
                await _handle_request(agent, follow_up)
            except Exception:
                logger.exception("Request failed; the session will continue.")

    except KeyboardInterrupt:
        logger.warning("Operation interrupted.")
    finally:
        # Ensure agent resources are cleaned up before exiting
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
