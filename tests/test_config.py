"""Tests for configuration module."""

import pytest
from pathlib import Path
import sys

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from flappy_ai.utils.config import Config


def test_config_initialization():
    """Test that config initializes correctly."""
    config = Config()

    assert config.WIN_WIDTH == 600
    assert config.WIN_HEIGHT == 800
    assert config.FLOOR_Y == 730
    assert config.FPS == 30


def test_config_paths():
    """Test that config paths are set correctly."""
    config = Config()

    assert config.ASSETS_DIR.exists()
    assert config.CONFIG_DIR.exists()
    assert config.CHECKPOINT_DIR.exists()
    assert config.LOGS_DIR.exists()


def test_config_to_dict():
    """Test config serialization to dict."""
    config = Config()
    config_dict = config.to_dict()

    assert "WIN_WIDTH" in config_dict
    assert "WIN_HEIGHT" in config_dict
    assert "FPS" in config_dict
    assert config_dict["WIN_WIDTH"] == 600
