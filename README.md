# NEAT Flappy Bird AI

A production-ready implementation of the NEAT (NeuroEvolution of Augmenting Topologies) algorithm for training an AI to play Flappy Bird. This project uses neural networks that evolve over generations to learn optimal gameplay strategies.

## Features

- **Production-Grade Code**: Modular architecture with proper separation of concerns
- **Type Hints**: Full type annotations for better code quality and IDE support
- **Comprehensive Logging**: Detailed logging with both console and file outputs
- **Error Handling**: Robust error handling throughout the application
- **CLI Interface**: Command-line interface with multiple options
- **Configuration Management**: Centralized configuration system
- **Pixel-Perfect Collision**: Advanced collision detection using Pygame masks
- **Neural Network Visualization**: Optional visualization of AI decision-making

## Project Structure

```
NEAT-Flappy-Bird/
├── src/
│   └── flappy_ai/
│       ├── __init__.py
│       ├── __main__.py
│       ├── main.py
│       ├── game/
│       │   ├── __init__.py
│       │   ├── bird.py          # Bird entity with physics
│       │   ├── pipe.py          # Pipe obstacles
│       │   ├── base.py          # Scrolling floor
│       │   └── game_engine.py   # Game loop and rendering
│       ├── ai/
│       │   ├── __init__.py
│       │   └── trainer.py       # NEAT training implementation
│       └── utils/
│           ├── __init__.py
│           ├── config.py        # Configuration management
│           ├── logger.py        # Logging setup
│           └── helpers.py       # Utility functions
├── config/
│   └── config-feedforward.txt   # NEAT algorithm configuration
├── assets/
│   ├── bird1.png, bird2.png, bird3.png
│   ├── pipe.png
│   ├── base.png
│   └── bg.png
├── checkpoints/                  # Saved trained models
├── logs/                        # Application logs
├── tests/                       # Unit tests
├── docs/                        # Additional documentation
├── requirements.txt
├── setup.py
└── README.md
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/NEAT-Flappy-Bird.git
   cd NEAT-Flappy-Bird
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the package (optional)**
   ```bash
   pip install -e .
   ```

## Usage

### Training the AI

**Basic training (50 generations):**
```bash
python -m flappy_ai.main train
```

**Custom number of generations:**
```bash
python -m flappy_ai.main train --generations 100
```

**Enable neural network visualization:**
```bash
python -m flappy_ai.main train --draw-lines
```

**Debug mode with detailed logging:**
```bash
python -m flappy_ai.main train --log-level DEBUG
```

**Disable file logging:**
```bash
python -m flappy_ai.main train --no-log-file
```

### Command-Line Options

```
positional arguments:
  {train}               Operation mode (currently only 'train' is supported)

optional arguments:
  -h, --help            Show this help message and exit
  --generations N       Maximum number of generations to train (default: 50)
  --config FILE         Path to NEAT configuration file
  --log-level LEVEL     Logging level: DEBUG, INFO, WARNING, ERROR (default: INFO)
  --draw-lines          Draw neural network input lines during training
  --no-log-file         Disable logging to file
```

## How It Works

### NEAT Algorithm

NEAT (NeuroEvolution of Augmenting Topologies) is a genetic algorithm that evolves neural networks. Instead of training with backpropagation, it:

1. **Initializes** a population of simple neural networks
2. **Evaluates** each network's fitness by playing Flappy Bird
3. **Selects** the best-performing networks
4. **Breeds** new networks through crossover and mutation
5. **Repeats** for multiple generations

### Neural Network Inputs

The AI receives three inputs:
- Bird's Y position
- Distance to top pipe
- Distance to bottom pipe

### Neural Network Output

A single output determines whether to jump:
- Output > 0.5: Jump
- Output ≤ 0.5: Don't jump

### Fitness Function

Birds are rewarded for:
- Staying alive (0.1 points per frame)
- Passing through pipes (5 points per pipe)

Birds are penalized for:
- Colliding with pipes (-1 point)

## Configuration

### NEAT Configuration

The `config/config-feedforward.txt` file controls the NEAT algorithm parameters:

- **Population size**: Number of birds per generation
- **Mutation rates**: How often networks change
- **Activation function**: Neural network activation (tanh)
- **Compatibility threshold**: Speciation parameters

### Application Configuration

Edit `src/flappy_ai/utils/config.py` to modify:

- Window dimensions
- Game speed (FPS)
- Physics parameters
- Asset paths

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

This project follows PEP 8 style guidelines:

```bash
# Check style
flake8 src/

# Format code
black src/
```

### Type Checking

```bash
mypy src/
```


