class ToolError(Exception):
    """Raised when a tool encounters an error."""

    def __init__(self, message):
        self.message = message


class OpenManusError(Exception):
    """Base exception for all OpenManus errors"""


class TokenLimitExceeded(OpenManusError):
    """Exception raised when the token limit is exceeded"""


class LLMEmptyResponseError(ValueError, OpenManusError):
    """Raised when the LLM returns an empty or invalid response.

    Subclasses ``ValueError`` so existing callers that already catch
    ``ValueError`` keep working, while still being distinguishable from
    deterministic input validation errors (which must not be retried).
    """
