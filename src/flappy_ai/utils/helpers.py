"""
Helper utility functions for the Flappy Bird AI application.
Author - Ritankar Saha
"""

import os
from pathlib import Path
from typing import Tuple, Optional, TYPE_CHECKING
import logging

if TYPE_CHECKING:
    import pygame

logger = logging.getLogger(__name__)


def load_image(
    filepath: Path,
    scale: Optional[Tuple[int, int]] = None,
    scale_factor: Optional[int] = None,
    convert_alpha: bool = True
) -> "pygame.Surface":
    """
    Load and optionally scale an image from disk.

    Args:
        filepath: Path to the image file
        scale: Tuple of (width, height) to scale to, or None
        scale_factor: Integer scale factor (e.g., 2 for 2x size), or None
        convert_alpha: Whether to convert image for alpha transparency

    Returns:
        Loaded and optionally scaled pygame Surface

    Raises:
        FileNotFoundError: If image file doesn't exist
        pygame.error: If image cannot be loaded
    """
    import pygame  # Import here to avoid circular imports and allow testing

    if not filepath.exists():
        raise FileNotFoundError(f"Image file not found: {filepath}")

    try:
        # Load the image
        if convert_alpha:
            image = pygame.image.load(str(filepath)).convert_alpha()
        else:
            image = pygame.image.load(str(filepath)).convert()

        # Apply scaling if requested
        if scale_factor:
            image = pygame.transform.scale2x(image) if scale_factor == 2 else \
                    pygame.transform.scale_by(image, scale_factor)
        elif scale:
            image = pygame.transform.scale(image, scale)

        logger.debug(f"Loaded image: {filepath.name}")
        return image

    except pygame.error as e:
        logger.error(f"Failed to load image {filepath}: {e}")
        raise


def rotate_and_blit(
    surface: "pygame.Surface",
    image: "pygame.Surface",
    top_left: Tuple[int, int],
    angle: float
) -> None:
    """
    Rotate an image and blit it to a surface, maintaining center position.

    This is used for rotating the bird sprite during gameplay.

    Args:
        surface: The surface to blit the rotated image onto
        image: The image to rotate
        top_left: The top-left position of the image before rotation
        angle: The angle to rotate the image (in degrees)
    """
    import pygame  # Import here to avoid circular imports

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center
    )
    surface.blit(rotated_image, new_rect.topleft)


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Clamp a value between a minimum and maximum.

    Args:
        value: Value to clamp
        min_value: Minimum allowed value
        max_value: Maximum allowed value

    Returns:
        Clamped value
    """
    return max(min_value, min(max_value, value))


def calculate_distance(
    point1: Tuple[float, float],
    point2: Tuple[float, float]
) -> float:
    """
    Calculate Euclidean distance between two points.

    Args:
        point1: First point (x, y)
        point2: Second point (x, y)

    Returns:
        Distance between the points
    """
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5


def format_time(seconds: float) -> str:
    """
    Format seconds into a readable time string.

    Args:
        seconds: Time in seconds

    Returns:
        Formatted time string (e.g., "1m 23s" or "45s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"
