class PRAnalyzerError(Exception):
    """Base exception for the application."""


class NotFoundError(PRAnalyzerError):
    pass


class ValidationError(PRAnalyzerError):
    pass
