"""Utility modules for configuration, logging, and helpers.
Author - Ritankar Saha"""

# Lazy imports to avoid importing pygame until needed
__all__ = ["Config", "setup_logger", "load_image", "rotate_and_blit"]


def __getattr__(name):
    """Lazy import of utilities."""
    if name == "Config":
        from .config import Config
        return Config
    elif name == "setup_logger":
        from .logger import setup_logger
        return setup_logger
    elif name == "load_image":
        from .helpers import load_image
        return load_image
    elif name == "rotate_and_blit":
        from .helpers import rotate_and_blit
        return rotate_and_blit
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
