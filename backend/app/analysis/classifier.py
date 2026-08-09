from pathlib import PurePosixPath


class FileClassifier:
    """Classifies changed files using deterministic path rules."""

    SECURITY_PATHS = {
        "auth",
        "authentication",
        "security",
        "permissions",
        "permission",
        "middleware",
        "oauth",
        "jwt",
    }

    DATABASE_PATHS = {
        "migration",
        "migrations",
        "database",
        "db",
        "models",
        "schema",
    }

    CI_PATHS = {
        ".github",
        ".gitlab",
        ".circleci",
        "jenkinsfile",
    }

    DEPENDENCY_FILES = {
        "package.json",
        "package-lock.json",
        "pnpm-lock.yaml",
        "yarn.lock",
        "requirements.txt",
        "requirements-dev.txt",
        "pyproject.toml",
        "poetry.lock",
        "pipfile",
        "pipfile.lock",
        "cargo.toml",
        "cargo.lock",
        "go.mod",
        "go.sum",
    }

    @classmethod
    def is_security_sensitive(cls, filename: str) -> bool:
        path = PurePosixPath(filename.lower())

        return any(
            part in cls.SECURITY_PATHS
            for part in path.parts
        )

    @classmethod
    def is_database_related(cls, filename: str) -> bool:
        path = PurePosixPath(filename.lower())

        if any(
            part in cls.DATABASE_PATHS
            for part in path.parts
        ):
            return True

        return (
            "migration" in path.name
            or path.name.endswith(".sql")
        )

    @classmethod
    def is_ci_related(cls, filename: str) -> bool:
        path = PurePosixPath(filename.lower())

        return any(
            part in cls.CI_PATHS
            for part in path.parts
        ) or path.name in {
            "dockerfile",
            "docker-compose.yml",
            "docker-compose.yaml",
        }

    @classmethod
    def is_dependency_file(cls, filename: str) -> bool:
        path = PurePosixPath(filename.lower())

        return path.name in cls.DEPENDENCY_FILES