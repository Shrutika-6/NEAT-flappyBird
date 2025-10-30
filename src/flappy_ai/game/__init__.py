"""Game components for Flappy Bird.
Author - Ritankar Saha
"""

# Lazy imports to avoid importing pygame until needed
__all__ = ["Bird", "Pipe", "Base", "GameEngine"]


def __getattr__(name):
    """Lazy import of game components."""
    if name == "Bird":
        from .bird import Bird
        return Bird
    elif name == "Pipe":
        from .pipe import Pipe
        return Pipe
    elif name == "Base":
        from .base import Base
        return Base
    elif name == "GameEngine":
        from .game_engine import GameEngine
        return GameEngine
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
