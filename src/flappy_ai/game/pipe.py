"""
Pipe class representing obstacles in Flappy Bird.
Author - Ritankar Saha
"""

import random
from typing import Tuple
import pygame
import logging

logger = logging.getLogger(__name__)


class Pipe:
    """
    Represents a pair of pipes (top and bottom) in Flappy Bird.

    Pipes move horizontally across the screen and have a gap between
    them for the bird to fly through.
    """

    GAP: int = 200  # Vertical gap between top and bottom pipes
    VEL: int = 5    # Horizontal velocity (pixels per frame)
    MIN_HEIGHT: int = 50   # Minimum pipe height from top
    MAX_HEIGHT: int = 450  # Maximum pipe height from top

    def __init__(self, x: int, pipe_img: pygame.Surface):
        """
        Initialize a pipe pair.

        Args:
            x: Starting x position
            pipe_img: Image for the bottom pipe (will be flipped for top)
        """
        self.x = x
        self.height = 0  # Height where gap starts
        self.top = 0     # Y position of top pipe
        self.bottom = 0  # Y position of bottom pipe

        # Create top and bottom pipe images
        self.PIPE_TOP = pygame.transform.flip(pipe_img, False, True)
        self.PIPE_BOTTOM = pipe_img

        self.passed = False  # Whether bird has passed this pipe
        self.set_height()

        logger.debug(f"Pipe created at x={x}, height={self.height}")

    def set_height(self) -> None:
        """
        Randomly set the height of the pipe gap.

        The height determines where the gap between pipes starts,
        making each pipe pair unique.
        """
        self.height = random.randrange(self.MIN_HEIGHT, self.MAX_HEIGHT)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self) -> None:
        """Move the pipe horizontally based on velocity."""
        self.x -= self.VEL

    def draw(self, win: pygame.Surface) -> None:
        """
        Draw both the top and bottom pipes.

        Args:
            win: Pygame window surface to draw on
        """
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird: "Bird") -> bool:
        """
        Check if the bird collides with this pipe using pixel-perfect collision.

        Args:
            bird: Bird object to check collision with

        Returns:
            True if collision detected, False otherwise
        """
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        # Calculate offsets for mask overlap
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # Check for overlap
        top_collision = bird_mask.overlap(top_mask, top_offset)
        bottom_collision = bird_mask.overlap(bottom_mask, bottom_offset)

        if top_collision or bottom_collision:
            logger.debug(f"Collision detected at pipe x={self.x}")
            return True

        return False

    def is_off_screen(self, screen_width: int = 0) -> bool:
        """
        Check if the pipe has moved off the left side of the screen.

        Args:
            screen_width: Width of the screen (unused, kept for compatibility)

        Returns:
            True if pipe is off screen, False otherwise
        """
        return self.x + self.PIPE_TOP.get_width() < 0

    def has_passed(self, bird_x: int) -> bool:
        """
        Check if the bird has passed this pipe.

        Args:
            bird_x: X position of the bird

        Returns:
            True if bird has passed the pipe, False otherwise
        """
        return not self.passed and self.x < bird_x

    def mark_passed(self) -> None:
        """Mark this pipe as passed by the bird."""
        self.passed = True
        logger.debug(f"Pipe at x={self.x} marked as passed")

    def get_top_pipe_rect(self) -> pygame.Rect:
        """
        Get the bounding rectangle of the top pipe.

        Returns:
            Pygame Rect for the top pipe
        """
        return self.PIPE_TOP.get_rect(topleft=(self.x, self.top))

    def get_bottom_pipe_rect(self) -> pygame.Rect:
        """
        Get the bounding rectangle of the bottom pipe.

        Returns:
            Pygame Rect for the bottom pipe
        """
        return self.PIPE_BOTTOM.get_rect(topleft=(self.x, self.bottom))

    def get_gap_center(self) -> Tuple[int, int]:
        """
        Get the center point of the gap between pipes.

        Returns:
            Tuple of (x, y) coordinates of the gap center
        """
        gap_y = self.height + self.GAP // 2
        gap_x = self.x + self.PIPE_TOP.get_width() // 2
        return (gap_x, gap_y)

    def __repr__(self) -> str:
        """String representation of the pipe."""
        return f"Pipe(x={self.x}, height={self.height}, passed={self.passed})"
