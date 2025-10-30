# Architecture Documentation

## Overview

This document describes the architecture of the NEAT Flappy Bird AI project, explaining the design decisions, module organization, and data flow.

## Project Structure

```
NEAT-Flappy-Bird/
├── src/flappy_ai/          # Main package
│   ├── game/               # Game entities and engine
│   ├── ai/                 # NEAT training implementation
│   ├── utils/              # Utilities (config, logging, helpers)
│   ├── main.py             # CLI entry point
│   ├── __main__.py         # Module execution support
│   └── __init__.py         # Package initialization
├── config/                 # Configuration files
├── assets/                 # Game assets (images)
├── checkpoints/            # Saved models
├── logs/                   # Application logs
├── tests/                  # Unit tests
└── docs/                   # Documentation
```

## Design Patterns

### 1. Separation of Concerns

The codebase is organized into distinct modules:

- **game/**: Pure game logic, independent of AI
- **ai/**: NEAT algorithm implementation, depends on game
- **utils/**: Shared utilities, no dependencies on game or AI

### 2. Dependency Injection

Configuration and game engine are injected into components:

```python
config = Config()
game = GameEngine(config)
trainer = NEATTrainer(config, game)
```

This allows for:
- Easy testing with mock objects
- Configuration flexibility
- Loose coupling between components

### 3. Context Managers

Resources are properly managed using context managers:

```python
with GameEngine(config) as game:
    # Resources automatically cleaned up
    trainer.train()
```

### 4. Lazy Imports

Pygame is imported lazily to:
- Allow testing without pygame
- Improve import times
- Enable type checking without runtime dependencies

## Module Descriptions

### Game Module

#### Bird (`game/bird.py`)
- Represents the player character
- Physics-based movement with gravity
- Animated sprites
- Collision detection via masks

**Key Methods:**
- `jump()`: Apply upward velocity
- `move()`: Update position based on physics
- `draw()`: Render with animation and rotation
- `get_mask()`: Return collision mask

#### Pipe (`game/pipe.py`)
- Represents obstacle pairs (top/bottom)
- Random gap positioning
- Pixel-perfect collision detection

**Key Methods:**
- `set_height()`: Randomize pipe gap
- `move()`: Horizontal scrolling
- `collide()`: Check bird collision
- `draw()`: Render both pipes

#### Base (`game/base.py`)
- Scrolling floor
- Infinite scrolling effect using two images

**Key Methods:**
- `move()`: Update scroll position
- `draw()`: Render seamless floor

#### GameEngine (`game/game_engine.py`)
- Central game management
- Asset loading and caching
- Rendering pipeline
- Event handling

**Key Methods:**
- `_load_assets()`: Load all game images
- `draw_window()`: Render complete game state
- `handle_events()`: Process pygame events
- `create_bird/pipe/base()`: Factory methods

### AI Module

#### NEATTrainer (`ai/trainer.py`)
- NEAT algorithm implementation
- Fitness evaluation
- Generation management
- Checkpoint saving

**Key Methods:**
- `train()`: Run evolution for N generations
- `_eval_genomes()`: Fitness function (called by NEAT)
- `_save_genome()`: Persist trained models
- `load_genome()`: Load saved models

**Fitness Function:**
- +0.1 per frame alive
- +5 per pipe passed
- -1 for collision

### Utils Module

#### Config (`utils/config.py`)
- Centralized configuration
- Path management
- Validation

**Key Attributes:**
- Window dimensions
- Game physics constants
- File paths
- NEAT settings

#### Logger (`utils/logger.py`)
- Structured logging
- File and console outputs
- Timestamps and formatting

#### Helpers (`utils/helpers.py`)
- Image loading and scaling
- Rotation and blitting
- Math utilities (clamp, distance)
- Time formatting

## Data Flow

### Training Loop

```
main.py
  ↓
NEATTrainer.train()
  ↓
NEAT Population.run()
  ↓
NEATTrainer._eval_genomes()  [for each generation]
  ↓
  ├─→ Create birds/networks
  ├─→ Game loop [while birds alive]
  │     ├─→ Bird.move()
  │     ├─→ Network.activate()  [get decision]
  │     ├─→ Bird.jump()  [if output > 0.5]
  │     ├─→ Pipe.collide()  [check collisions]
  │     ├─→ Update fitness
  │     └─→ GameEngine.draw_window()
  └─→ Save best genome
```

### Neural Network I/O

**Inputs (3):**
1. Bird's Y position
2. Distance to top pipe
3. Distance to bottom pipe

**Processing:**
- FeedForward network (no recurrent connections)
- Tanh activation function
- Evolved topology (starts simple, grows complex)

**Output (1):**
- Single value between -1 and 1
- > 0.5: Jump
- ≤ 0.5: Don't jump

## Configuration System

### Application Config (`Config` class)
- Window dimensions
- Game speed (FPS)
- Display settings
- Asset paths

### NEAT Config (`config-feedforward.txt`)
- Population size
- Mutation rates
- Activation functions
- Speciation parameters
- Reproduction settings

## Error Handling Strategy

### Layered Approach

1. **Module Level**: Catch specific errors where they occur
2. **Function Level**: Validate inputs, raise descriptive exceptions
3. **Application Level**: Top-level try/catch in main()
4. **Logging**: All errors logged with context

### Error Categories

- **Configuration Errors**: Missing files, invalid settings
- **Runtime Errors**: Pygame issues, collision bugs
- **NEAT Errors**: Population extinction, convergence issues

## Performance Considerations

### Optimizations

1. **Lazy Imports**: Reduce startup time
2. **Asset Caching**: Load images once at startup
3. **Mask Caching**: Reuse collision masks
4. **Vectorization**: Use numpy for calculations

### Bottlenecks

1. **Rendering**: Can slow with many birds
   - Solution: Increase FPS or disable visualization
2. **Network Evaluation**: Grows with population
   - Solution: Reduce population size
3. **Collision Detection**: Pixel-perfect masks are expensive
   - Acceptable trade-off for accuracy

## Testing Strategy

### Unit Tests
- Configuration validation
- Helper function correctness
- Math utilities

### Integration Tests
- Game loop execution
- NEAT algorithm convergence
- Checkpoint save/load

### Manual Tests
- Visual inspection of game
- Neural network behavior
- Performance profiling

## Extension Points

### Adding New Game Modes
1. Create new mode in `main.py`
2. Implement mode logic
3. Add CLI argument

### Custom Fitness Functions
1. Modify `_eval_genomes()` in `trainer.py`
2. Adjust reward/penalty values
3. Add new input features

### Alternative Algorithms
1. Create new trainer in `ai/`
2. Implement same interface as `NEATTrainer`
3. Add option to CLI

## Dependencies

### Core
- **pygame**: Game rendering and input
- **neat-python**: NEAT algorithm implementation
- **numpy**: Numerical operations

### Utilities
- **matplotlib**: Fitness visualization (visualize.py)
- **graphviz**: Network topology visualization

### Development
- **pytest**: Testing framework
- **black**: Code formatting
- **mypy**: Type checking
- **flake8**: Linting

## Future Improvements

1. **Parallel Evaluation**: Run multiple birds in parallel
2. **GPU Acceleration**: Use PyTorch/JAX for networks
3. **Replay System**: Save and replay best runs
4. **Web Interface**: Browser-based visualization
5. **Hyperparameter Tuning**: Automated config optimization
6. **Transfer Learning**: Start from pre-trained models
