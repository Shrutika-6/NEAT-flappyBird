"""
AI-powered Flappy Bird game using NEAT algorithm.
"""

__version__ = "1.0.0"
__author__ = "Tech With Tim (Refactored)"

# Lazy imports to avoid importing pygame until needed
__all__ = [
    "Bird",
    "Pipe",
    "Base",
    "GameEngine",
    "NEATTrainer",
    "Config",
    "setup_logger",
]


def __getattr__(name):
    """Lazy import of submodules."""
    if name == "Bird":
        from .game.bird import Bird
        return Bird
    elif name == "Pipe":
        from .game.pipe import Pipe
        return Pipe
    elif name == "Base":
        from .game.base import Base
        return Base
    elif name == "GameEngine":
        from .game.game_engine import GameEngine
        return GameEngine
    elif name == "NEATTrainer":
        from .ai.trainer import NEATTrainer
        return NEATTrainer
    elif name == "Config":
        from .utils.config import Config
        return Config
    elif name == "setup_logger":
        from .utils.logger import setup_logger
        return setup_logger
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
