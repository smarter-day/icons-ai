"""Languages management."""


from typing import Any


def load_languages(languages: str, settings: Any) -> list[str]:
    """Load languages from a string or from the project settings."""
    if languages:
        return [lang.strip() for lang in languages.split(",") if lang.strip()]

    if settings and hasattr(settings, "languages"):
        return [lang.code for lang in settings.languages]

    return []
