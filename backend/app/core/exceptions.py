class PRAnalyzerError(Exception):
    """Base exception for the application."""


class NotFoundError(PRAnalyzerError):
    pass


class ValidationError(PRAnalyzerError):
    pass


class RepositoryAlreadyExistsError(Exception):
    """Raised when attempting to create a repository that already exists."""

    pass
