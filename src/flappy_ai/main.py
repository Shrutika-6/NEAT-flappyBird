"""
Main entry point for the NEAT Flappy Bird AI application.
"""

import argparse
import sys
import logging
from pathlib import Path

from .utils.config import Config
from .utils.logger import setup_logger
from .game.game_engine import GameEngine
from .ai.trainer import NEATTrainer


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="NEAT Flappy Bird AI - Train neural networks to play Flappy Bird",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Train a new AI
  python -m flappy_ai.main train

  # Train with custom configuration
  python -m flappy_ai.main train --generations 100 --config custom_config.txt

  # Train with debug logging
  python -m flappy_ai.main train --log-level DEBUG

  # Show neural network visualization
  python -m flappy_ai.main train --draw-lines
        """
    )

    parser.add_argument(
        "mode",
        choices=["train"],
        help="Operation mode (currently only 'train' is supported)"
    )

    parser.add_argument(
        "--generations",
        type=int,
        default=50,
        help="Maximum number of generations to train (default: 50)"
    )

    parser.add_argument(
        "--config",
        type=str,
        help="Path to NEAT configuration file (default: config/config-feedforward.txt)"
    )

    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)"
    )

    parser.add_argument(
        "--draw-lines",
        action="store_true",
        help="Draw neural network input lines during training"
    )

    parser.add_argument(
        "--no-log-file",
        action="store_true",
        help="Disable logging to file"
    )

    return parser.parse_args()


def main() -> int:
    """
    Main application entry point.

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    # Parse arguments
    args = parse_args()

    # Set up logging
    log_level = getattr(logging, args.log_level)
    log_dir = None if args.no_log_file else Path("logs")

    logger = setup_logger(
        level=log_level,
        log_dir=log_dir,
        console=True
    )

    logger.info("="*60)
    logger.info("NEAT Flappy Bird AI")
    logger.info("="*60)

    try:
        # Initialize configuration
        config = Config()

        # Set draw lines if requested
        if args.draw_lines:
            config.DRAW_LINES = True
            logger.info("Neural network visualization enabled")

        # Set custom config path if provided
        if args.config:
            config.NEAT_CONFIG_FILE = Path(args.config)

        # Set max generations
        config.MAX_GENERATIONS = args.generations

        logger.info(f"Configuration: {config.to_dict()}")

        # Run training mode
        if args.mode == "train":
            logger.info(f"Starting training for {args.generations} generations")

            # Initialize game engine
            with GameEngine(config) as game:
                # Initialize trainer
                trainer = NEATTrainer(config, game)

                # Start training
                winner = trainer.train(
                    config.NEAT_CONFIG_FILE,
                    max_generations=args.generations
                )

                logger.info(f"Training complete! Best fitness: {winner.fitness:.2f}")

        logger.info("="*60)
        logger.info("Application completed successfully")
        logger.info("="*60)

        return 0

    except KeyboardInterrupt:
        logger.info("\nApplication interrupted by user")
        return 130  # Standard exit code for SIGINT

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return 1

    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
