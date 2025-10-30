"""AI training components using NEAT algorithm."""

# Lazy imports to avoid importing pygame until needed
__all__ = ["NEATTrainer"]


def __getattr__(name):
    """Lazy import of AI components."""
    if name == "NEATTrainer":
        from .trainer import NEATTrainer
        return NEATTrainer
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
