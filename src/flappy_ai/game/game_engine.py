"""
Game engine managing the Flappy Bird game state and rendering.
Author - Ritankar Saha
"""

from typing import List, Optional, Tuple
import pygame
import logging

from .bird import Bird
from .pipe import Pipe
from .base import Base
from ..utils.config import Config

logger = logging.getLogger(__name__)


class GameEngine:
    """
    Manages game state, rendering, and game logic for Flappy Bird.

    This class handles the game window, asset loading, rendering,
    and provides an interface for the AI trainer.
    """

    def __init__(self, config: Config):
        """
        Initialize the game engine.

        Args:
            config: Configuration object with game settings
        """
        self.config = config

        # Initialize Pygame
        pygame.init()
        pygame.font.init()

        # Create game window
        self.window = pygame.display.set_mode(
            (config.WIN_WIDTH, config.WIN_HEIGHT)
        )
        pygame.display.set_caption("NEAT Flappy Bird AI")

        # Load assets
        self._load_assets()

        # Initialize fonts
        self.stat_font = pygame.font.SysFont(
            config.FONT_NAME,
            config.STAT_FONT_SIZE
        )
        self.end_font = pygame.font.SysFont(
            config.FONT_NAME,
            config.END_FONT_SIZE
        )

        # Game clock
        self.clock = pygame.time.Clock()

        logger.info("Game engine initialized")

    def _load_assets(self) -> None:
        """Load all game assets (images)."""
        from ..utils.helpers import load_image

        try:
            # Load bird images for animation
            self.bird_images = [
                load_image(
                    self.config.get_image_path(f"bird{i}.png"),
                    scale_factor=self.config.IMAGE_SCALE
                )
                for i in range(1, 4)
            ]

            # Load pipe image
            self.pipe_image = load_image(
                self.config.get_image_path("pipe.png"),
                scale_factor=self.config.IMAGE_SCALE
            )

            # Load base image
            self.base_image = load_image(
                self.config.get_image_path("base.png"),
                scale_factor=self.config.IMAGE_SCALE
            )

            # Load background image
            self.bg_image = load_image(
                self.config.get_image_path("bg.png"),
                scale=(self.config.WIN_WIDTH, 900)
            )

            logger.info("All game assets loaded successfully")

        except Exception as e:
            logger.error(f"Failed to load game assets: {e}")
            raise

    def create_bird(self, x: int = 230, y: int = 350) -> Bird:
        """
        Create a new bird instance.

        Args:
            x: Starting x position
            y: Starting y position

        Returns:
            New Bird instance
        """
        return Bird(x, y, self.bird_images)

    def create_pipe(self, x: int) -> Pipe:
        """
        Create a new pipe instance.

        Args:
            x: Starting x position

        Returns:
            New Pipe instance
        """
        return Pipe(x, self.pipe_image)

    def create_base(self) -> Base:
        """
        Create a new base instance.

        Returns:
            New Base instance
        """
        return Base(self.config.FLOOR_Y, self.base_image)

    def draw_window(
        self,
        birds: List[Bird],
        pipes: List[Pipe],
        base: Base,
        score: int,
        generation: int,
        pipe_index: int = 0
    ) -> None:
        """
        Render the complete game state to the window.

        Args:
            birds: List of active bird instances
            pipes: List of pipe instances
            base: Base instance
            score: Current score
            generation: Current generation number
            pipe_index: Index of the pipe to draw neural network lines to
        """
        # Draw background
        self.window.blit(self.bg_image, (0, 0))

        # Draw pipes
        for pipe in pipes:
            pipe.draw(self.window)

        # Draw base
        base.draw(self.window)

        # Draw birds and optional neural network lines
        for bird in birds:
            if self.config.DRAW_LINES and pipes:
                self._draw_neural_network_lines(bird, pipes, pipe_index)
            bird.draw(self.window)

        # Draw statistics
        self._draw_stats(score, generation, len(birds))

        # Update display
        pygame.display.update()

    def _draw_neural_network_lines(
        self,
        bird: Bird,
        pipes: List[Pipe],
        pipe_index: int
    ) -> None:
        """
        Draw lines from bird to pipes showing neural network inputs.

        Args:
            bird: Bird instance
            pipes: List of pipe instances
            pipe_index: Index of the target pipe
        """
        if pipe_index >= len(pipes):
            return

        try:
            pipe = pipes[pipe_index]
            bird_center = (
                bird.x + bird.img.get_width() / 2,
                bird.y + bird.img.get_height() / 2
            )

            # Line to top pipe
            top_point = (
                pipe.x + pipe.PIPE_TOP.get_width() / 2,
                pipe.height
            )
            pygame.draw.line(
                self.window,
                (255, 0, 0),
                bird_center,
                top_point,
                5
            )

            # Line to bottom pipe
            bottom_point = (
                pipe.x + pipe.PIPE_BOTTOM.get_width() / 2,
                pipe.bottom
            )
            pygame.draw.line(
                self.window,
                (255, 0, 0),
                bird_center,
                bottom_point,
                5
            )

        except Exception as e:
            logger.debug(f"Could not draw neural network lines: {e}")

    def _draw_stats(
        self,
        score: int,
        generation: int,
        alive_count: int
    ) -> None:
        """
        Draw game statistics on the screen.

        Args:
            score: Current score
            generation: Current generation number
            alive_count: Number of birds still alive
        """
        # Score (top right)
        score_label = self.stat_font.render(
            f"Score: {score}",
            True,
            (255, 255, 255)
        )
        self.window.blit(
            score_label,
            (self.config.WIN_WIDTH - score_label.get_width() - 15, 10)
        )

        # Generation (top left)
        gen_label = self.stat_font.render(
            f"Gen: {generation}",
            True,
            (255, 255, 255)
        )
        self.window.blit(gen_label, (10, 10))

        # Alive count (below generation)
        alive_label = self.stat_font.render(
            f"Alive: {alive_count}",
            True,
            (255, 255, 255)
        )
        self.window.blit(alive_label, (10, 50))

    def tick(self, fps: Optional[int] = None) -> None:
        """
        Tick the game clock to maintain frame rate.

        Args:
            fps: Frames per second (uses config default if None)
        """
        if fps is None:
            fps = self.config.FPS
        self.clock.tick(fps)

    def handle_events(self) -> bool:
        """
        Handle pygame events.

        Returns:
            False if quit event detected, True otherwise
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.info("Quit event detected")
                return False
        return True

    def cleanup(self) -> None:
        """Clean up pygame resources."""
        pygame.quit()
        logger.info("Game engine cleaned up")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
