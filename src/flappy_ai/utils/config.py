"""
Configuration management for the Flappy Bird AI application.
Author - Ritankar Saha
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class Config:
    """
    Centralized configuration management for the application.

    This class manages all configuration settings including game parameters,
    display settings, NEAT configuration, and file paths.
    """

    # Game window settings
    WIN_WIDTH: int = 600
    WIN_HEIGHT: int = 800
    FLOOR_Y: int = 730
    FPS: int = 30

    # Display settings
    DRAW_LINES: bool = False  # Draw neural network input lines
    STAT_FONT_SIZE: int = 50
    END_FONT_SIZE: int = 70
    FONT_NAME: str = "comicsans"

    # Asset paths
    ASSETS_DIR: Path
    IMGS_DIR: Path
    CONFIG_DIR: Path
    CHECKPOINT_DIR: Path
    LOGS_DIR: Path

    # Image scale factor
    IMAGE_SCALE: int = 2

    # NEAT configuration
    NEAT_CONFIG_FILE: Path
    MAX_GENERATIONS: int = 50

    # Training settings
    FITNESS_THRESHOLD: int = 100
    SCORE_CHECKPOINT: int = 20  # Save checkpoint when this score is reached

    def __init__(self, base_dir: Optional[Path] = None):
        """
        Initialize configuration with base directory.

        Args:
            base_dir: Base directory of the project. If None, uses the project root.
        """
        if base_dir is None:
            # Get the project root (3 levels up from this file)
            base_dir = Path(__file__).parent.parent.parent.parent

        self.base_dir = Path(base_dir).resolve()

        # Set up directory paths
        self.ASSETS_DIR = self.base_dir / "assets"
        self.IMGS_DIR = self.ASSETS_DIR
        self.CONFIG_DIR = self.base_dir / "config"
        self.CHECKPOINT_DIR = self.base_dir / "checkpoints"
        self.LOGS_DIR = self.base_dir / "logs"

        # Create directories if they don't exist
        self._create_directories()

        # Set NEAT config path
        self.NEAT_CONFIG_FILE = self.CONFIG_DIR / "config-feedforward.txt"

        # Validate configuration
        self._validate()

        logger.info(f"Configuration initialized with base directory: {self.base_dir}")

    def _create_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        directories = [
            self.ASSETS_DIR,
            self.CONFIG_DIR,
            self.CHECKPOINT_DIR,
            self.LOGS_DIR,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def _validate(self) -> None:
        """
        Validate that all required files and directories exist.

        Raises:
            FileNotFoundError: If required files or directories are missing
        """
        # Check assets directory
        if not self.IMGS_DIR.exists():
            raise FileNotFoundError(f"Assets directory not found: {self.IMGS_DIR}")

        # Check for required image files
        required_images = ["bird1.png", "bird2.png", "bird3.png", "pipe.png", "base.png", "bg.png"]
        missing_images = []

        for img in required_images:
            img_path = self.IMGS_DIR / img
            if not img_path.exists():
                missing_images.append(img)

        if missing_images:
            raise FileNotFoundError(
                f"Missing required image files in {self.IMGS_DIR}: {', '.join(missing_images)}"
            )

        # Check NEAT config file
        if not self.NEAT_CONFIG_FILE.exists():
            raise FileNotFoundError(
                f"NEAT configuration file not found: {self.NEAT_CONFIG_FILE}"
            )

        logger.info("Configuration validation passed")

    def get_image_path(self, filename: str) -> Path:
        """
        Get the full path to an image file.

        Args:
            filename: Name of the image file

        Returns:
            Full path to the image file
        """
        return self.IMGS_DIR / filename

    def get_checkpoint_path(self, filename: str) -> Path:
        """
        Get the full path to a checkpoint file.

        Args:
            filename: Name of the checkpoint file

        Returns:
            Full path to the checkpoint file
        """
        return self.CHECKPOINT_DIR / filename

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to a dictionary.

        Returns:
            Dictionary of configuration values
        """
        return {
            "WIN_WIDTH": self.WIN_WIDTH,
            "WIN_HEIGHT": self.WIN_HEIGHT,
            "FLOOR_Y": self.FLOOR_Y,
            "FPS": self.FPS,
            "DRAW_LINES": self.DRAW_LINES,
            "MAX_GENERATIONS": self.MAX_GENERATIONS,
            "FITNESS_THRESHOLD": self.FITNESS_THRESHOLD,
            "base_dir": str(self.base_dir),
        }

    def __repr__(self) -> str:
        """String representation of the configuration."""
        return f"Config(base_dir={self.base_dir})"
