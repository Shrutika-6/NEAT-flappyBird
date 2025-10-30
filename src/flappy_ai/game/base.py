"""
Base class representing the moving floor in Flappy Bird.
Author - Ritankar Saha
"""

import pygame
import logging

logger = logging.getLogger(__name__)


class Base:
    """
    Represents the scrolling floor/base of the game.

    The base uses two images that scroll together to create
    an infinite scrolling effect.
    """

    VEL: int = 5  # Horizontal velocity (should match pipe velocity)

    def __init__(self, y: int, image: pygame.Surface):
        """
        Initialize the base.

        Args:
            y: Vertical position of the base
            image: Image for the base
        """
        self.y = y
        self.image = image
        self.width = image.get_width()

        # Two x positions for seamless scrolling
        self.x1 = 0
        self.x2 = self.width

        logger.debug(f"Base initialized at y={y}, width={self.width}")

    def move(self) -> None:
        """
        Move the base to create scrolling effect.

        Uses two images that cycle positions for infinite scrolling.
        """
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        # Reset first image when it goes off screen
        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        # Reset second image when it goes off screen
        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, win: pygame.Surface) -> None:
        """
        Draw both base images to create seamless scrolling.

        Args:
            win: Pygame window surface to draw on
        """
        win.blit(self.image, (self.x1, self.y))
        win.blit(self.image, (self.x2, self.y))

    def get_collision_y(self) -> int:
        """
        Get the y-coordinate where collision should be detected.

        Returns:
            Y position of the top of the base
        """
        return self.y

    def reset(self) -> None:
        """Reset base to initial positions."""
        self.x1 = 0
        self.x2 = self.width
        logger.debug("Base reset to initial positions")

    def __repr__(self) -> str:
        """String representation of the base."""
        return f"Base(y={self.y}, x1={self.x1}, x2={self.x2})"
