class WebhookDependencyPending(Exception):
    """Raised when a webhook depends on data not synchronized yet."""

    def __init__(self, message: str):
        super().__init__(message)