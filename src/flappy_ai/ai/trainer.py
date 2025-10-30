"""
NEAT trainer for training neural networks to play Flappy Bird.
Author - Ritankar Saha
"""

from typing import List, Tuple, Optional
import neat
import pickle
import logging
from pathlib import Path

from ..game.game_engine import GameEngine
from ..game.bird import Bird
from ..game.pipe import Pipe
from ..game.base import Base
from ..utils.config import Config

logger = logging.getLogger(__name__)


class NEATTrainer:
    """
    Handles NEAT algorithm training for Flappy Bird AI.

    This class manages the training loop, fitness evaluation,
    and checkpoint saving for the neural network evolution.
    """

    def __init__(self, config: Config, game_engine: GameEngine):
        """
        Initialize the NEAT trainer.

        Args:
            config: Application configuration
            game_engine: Game engine instance
        """
        self.config = config
        self.game = game_engine
        self.generation = 0
        self.best_genome = None
        self.best_fitness = float('-inf')

        logger.info("NEAT Trainer initialized")

    def train(
        self,
        neat_config_path: Path,
        max_generations: Optional[int] = None
    ) -> neat.DefaultGenome:
        """
        Run the NEAT training algorithm.

        Args:
            neat_config_path: Path to NEAT configuration file
            max_generations: Maximum generations to train (uses config default if None)

        Returns:
            Best genome found during training
        """
        if max_generations is None:
            max_generations = self.config.MAX_GENERATIONS

        # Load NEAT configuration
        neat_config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            str(neat_config_path)
        )

        # Create population
        population = neat.Population(neat_config)

        # Add reporters
        population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        population.add_reporter(stats)

        # Optional: Add checkpointer
        # checkpoint_freq = 5
        # population.add_reporter(
        #     neat.Checkpointer(
        #         checkpoint_freq,
        #         filename_prefix=str(self.config.CHECKPOINT_DIR / 'neat-checkpoint-')
        #     )
        # )

        logger.info(f"Starting training for {max_generations} generations")

        try:
            # Run evolution
            winner = population.run(self._eval_genomes, max_generations)

            # Save best genome
            self._save_genome(winner, "winner")

            logger.info(f"Training completed. Best fitness: {winner.fitness}")
            logger.info(f"Best genome:\n{winner}")

            return winner

        except KeyboardInterrupt:
            logger.info("Training interrupted by user")
            if self.best_genome:
                self._save_genome(self.best_genome, "interrupted_best")
            raise

        except Exception as e:
            logger.error(f"Training failed: {e}", exc_info=True)
            raise

    def _eval_genomes(
        self,
        genomes: List[Tuple[int, neat.DefaultGenome]],
        neat_config: neat.Config
    ) -> None:
        """
        Evaluate fitness of all genomes in the current generation.

        This is the fitness function called by NEAT for each generation.

        Args:
            genomes: List of (genome_id, genome) tuples
            neat_config: NEAT configuration object
        """
        self.generation += 1
        logger.info(f"\n{'='*60}")
        logger.info(f"Starting Generation {self.generation}")
        logger.info(f"{'='*60}")

        # Initialize neural networks and birds for each genome
        networks = []
        birds = []
        genome_list = []

        for genome_id, genome in genomes:
            genome.fitness = 0  # Start with fitness 0
            net = neat.nn.FeedForwardNetwork.create(genome, neat_config)
            networks.append(net)
            birds.append(self.game.create_bird())
            genome_list.append(genome)

        # Initialize game objects
        base = self.game.create_base()
        pipes = [self.game.create_pipe(700)]
        score = 0

        # Game loop
        run = True
        while run and len(birds) > 0:
            self.game.tick()

            # Handle events
            if not self.game.handle_events():
                run = False
                break

            # Determine which pipe to use for neural network input
            pipe_index = 0
            if len(birds) > 0:
                if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                    pipe_index = 1

            # Move birds and get neural network decisions
            for i, bird in enumerate(birds):
                bird.move()
                genome_list[i].fitness += 0.1  # Reward for staying alive

                # Get neural network output
                output = networks[i].activate((
                    bird.y,
                    abs(bird.y - pipes[pipe_index].height),
                    abs(bird.y - pipes[pipe_index].bottom)
                ))

                # Jump if output > 0.5
                if output[0] > 0.5:
                    bird.jump()

            # Move base
            base.move()

            # Process pipes
            add_pipe = False
            pipes_to_remove = []

            for pipe in pipes:
                pipe.move()

                # Check collisions
                for i, bird in enumerate(birds):
                    if pipe.collide(bird):
                        genome_list[i].fitness -= 1  # Penalty for collision
                        self._remove_bird(i, birds, networks, genome_list)

                # Remove pipes that are off screen
                if pipe.is_off_screen():
                    pipes_to_remove.append(pipe)

                # Check if bird passed pipe
                if not pipe.passed and len(birds) > 0 and pipe.x < birds[0].x:
                    pipe.mark_passed()
                    add_pipe = True

            # Add new pipe when bird passes old one
            if add_pipe:
                score += 1
                logger.info(f"Gen {self.generation}: Score reached {score}")

                # Reward all remaining birds
                for genome in genome_list:
                    genome.fitness += 5

                pipes.append(self.game.create_pipe(self.config.WIN_WIDTH))

            # Remove off-screen pipes
            for pipe in pipes_to_remove:
                pipes.remove(pipe)

            # Check for ground/ceiling collision
            for i in range(len(birds) - 1, -1, -1):
                bird = birds[i]
                if bird.y + bird.img.get_height() >= self.config.FLOOR_Y or bird.y < -50:
                    self._remove_bird(i, birds, networks, genome_list)

            # Draw everything
            self.game.draw_window(
                birds,
                pipes,
                base,
                score,
                self.generation,
                pipe_index
            )

        # Track best genome
        for genome in genome_list:
            if genome.fitness > self.best_fitness:
                self.best_fitness = genome.fitness
                self.best_genome = genome
                logger.info(f"New best fitness: {self.best_fitness:.2f}")

        logger.info(f"Generation {self.generation} completed with score: {score}")

    def _remove_bird(
        self,
        index: int,
        birds: List[Bird],
        networks: List,
        genomes: List[neat.DefaultGenome]
    ) -> None:
        """
        Remove a bird and its associated network and genome.

        Args:
            index: Index of bird to remove
            birds: List of birds
            networks: List of neural networks
            genomes: List of genomes
        """
        if 0 <= index < len(birds):
            birds.pop(index)
            networks.pop(index)
            genomes.pop(index)

    def _save_genome(
        self,
        genome: neat.DefaultGenome,
        name: str = "best"
    ) -> None:
        """
        Save a genome to disk.

        Args:
            genome: Genome to save
            name: Name for the save file
        """
        try:
            filepath = self.config.get_checkpoint_path(f"{name}.pickle")
            with open(filepath, 'wb') as f:
                pickle.dump(genome, f)
            logger.info(f"Genome saved to {filepath}")

        except Exception as e:
            logger.error(f"Failed to save genome: {e}")

    def load_genome(self, filename: str) -> neat.DefaultGenome:
        """
        Load a genome from disk.

        Args:
            filename: Name of the genome file

        Returns:
            Loaded genome

        Raises:
            FileNotFoundError: If genome file doesn't exist
        """
        filepath = self.config.get_checkpoint_path(filename)

        if not filepath.exists():
            raise FileNotFoundError(f"Genome file not found: {filepath}")

        try:
            with open(filepath, 'rb') as f:
                genome = pickle.load(f)
            logger.info(f"Genome loaded from {filepath}")
            return genome

        except Exception as e:
            logger.error(f"Failed to load genome: {e}")
            raise
