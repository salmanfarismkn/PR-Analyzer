import os


def is_test_file(filename: str) -> bool:
    """
    Identify test files by path or extension.
    Examples:
    - files under 'tests/' or '__tests__/'
    - files ending with .test.ts, .spec.ts, etc.
    """
    lower = filename.lower()
    return (
        "tests/" in lower
        or "__tests__/" in lower
        or lower.endswith(".test.ts")
        or lower.endswith(".spec.ts")
        or "test_" in os.path.basename(lower)
    )


def is_documentation(filename: str) -> bool:
    """
    Identify documentation files.
    Examples:
    - Markdown (.md), reStructuredText (.rst), text (.txt)
    - Files under 'docs/' directory
    """
    lower = filename.lower()
    return (
        lower.endswith((".md", ".rst", ".txt"))
        or "docs/" in lower
    )


def is_configuration(filename: str) -> bool:
    """
    Identify configuration files.
    Examples:
    - YAML, JSON, TOML, INI
    - Common config filenames like Dockerfile, Makefile
    """
    lower = filename.lower()
    return (
        lower.endswith((".yml", ".yaml", ".json", ".toml", ".ini"))
        or os.path.basename(lower) in {"dockerfile", "makefile"}
    )


def is_binary(filename: str) -> bool:
    """
    Identify binary files.
    Examples:
    - Images, executables, archives
    """
    lower = filename.lower()
    return lower.endswith((
        ".png", ".jpg", ".jpeg", ".gif", ".bmp",
        ".exe", ".dll", ".so",
        ".zip", ".tar", ".gz"
    ))
