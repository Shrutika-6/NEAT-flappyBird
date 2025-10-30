"""
Bird class representing the Flappy Bird character.
Author - Ritankar Saha
"""

from typing import List, Tuple
import pygame
import logging

from ..utils.helpers import rotate_and_blit

logger = logging.getLogger(__name__)


class Bird:
    """
    Represents the bird character in Flappy Bird.

    The bird has physics-based movement with gravity, jumping mechanics,
    and animated sprites.
    """

    # Class constants
    MAX_ROTATION: int = 25  # Maximum upward tilt angle
    ROT_VEL: int = 20       # Rotation velocity when falling
    ANIMATION_TIME: int = 5  # Frames per animation image
    JUMP_VELOCITY: float = -10.5  # Initial velocity when jumping
    GRAVITY: float = 3.0     # Gravity acceleration

    def __init__(
        self,
        x: int,
        y: int,
        images: List[pygame.Surface]
    ):
        """
        Initialize the bird.

        Args:
            x: Starting x position
            y: Starting y position
            images: List of bird sprite images for animation
        """
        self.x = x
        self.y = y
        self.tilt = 0  # Current tilt angle in degrees
        self.tick_count = 0  # Frames since last jump
        self.vel = 0  # Current vertical velocity
        self.height = self.y  # Height when last jumped
        self.img_count = 0  # Frame counter for animation
        self.images = images
        self.img = self.images[0]

        logger.debug(f"Bird initialized at position ({x}, {y})")

    def jump(self) -> None:
        """
        Make the bird jump by setting negative velocity.

        Resets the tick count and records the current height.
        """
        self.vel = self.JUMP_VELOCITY
        self.tick_count = 0
        self.height = self.y
        logger.debug(f"Bird jumped at y={self.y}")

    def move(self) -> None:
        """
        Update the bird's position based on physics.

        Applies gravity and calculates displacement using kinematic equations.
        Updates the bird's tilt based on movement direction.
        """
        self.tick_count += 1

        # Calculate displacement using physics formula: d = v*t + 0.5*a*t^2
        displacement = (
            self.vel * self.tick_count +
            0.5 * self.GRAVITY * self.tick_count ** 2
        )

        # Apply terminal velocity
        if displacement >= 16:
            displacement = (displacement / abs(displacement)) * 16

        # Extra boost when moving upward
        if displacement < 0:
            displacement -= 2

        # Update position
        self.y = self.y + displacement

        # Update tilt based on movement
        if displacement < 0 or self.y < self.height + 50:
            # Tilt up when jumping or moving upward
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            # Tilt down when falling
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win: pygame.Surface) -> None:
        """
        Draw the bird on the window with animation and rotation.

        Args:
            win: Pygame window surface to draw on
        """
        self.img_count += 1

        # Cycle through animation frames
        animation_cycle = self.ANIMATION_TIME * 4

        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.images[0]
        elif self.img_count <= self.ANIMATION_TIME * 2:
            self.img = self.images[1]
        elif self.img_count <= self.ANIMATION_TIME * 3:
            self.img = self.images[2]
        elif self.img_count <= self.ANIMATION_TIME * 4:
            self.img = self.images[1]
        elif self.img_count == animation_cycle + 1:
            self.img = self.images[0]
            self.img_count = 0

        # Don't flap when nose diving
        if self.tilt <= -80:
            self.img = self.images[1]
            self.img_count = self.ANIMATION_TIME * 2

        # Rotate and draw the bird
        rotate_and_blit(win, self.img, (self.x, self.y), self.tilt)

    def get_mask(self) -> pygame.mask.Mask:
        """
        Get the collision mask for the current bird image.

        Returns:
            Pygame mask for pixel-perfect collision detection
        """
        return pygame.mask.from_surface(self.img)

    def get_rect(self) -> pygame.Rect:
        """
        Get the bounding rectangle of the bird.

        Returns:
            Pygame Rect representing the bird's bounding box
        """
        return self.img.get_rect(topleft=(self.x, self.y))

    def reset(self, x: int, y: int) -> None:
        """
        Reset the bird to initial state at given position.

        Args:
            x: Reset x position
            y: Reset y position
        """
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.images[0]
        logger.debug(f"Bird reset to position ({x}, {y})")

    def __repr__(self) -> str:
        """String representation of the bird."""
        return f"Bird(x={self.x}, y={self.y:.1f}, vel={self.vel:.1f})"
