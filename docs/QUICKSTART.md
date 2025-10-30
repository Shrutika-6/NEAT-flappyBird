# Quick Start Guide

## Installation (< 2 minutes)

```bash
# Clone and enter directory
cd NEAT-Flappy-Bird

# Install dependencies
pip install -r requirements.txt

# Optional: Install as package
pip install -e .
```

## Run Training (Immediately)

```bash
# Start training with default settings (50 generations)
python -m flappy_ai.main train
```

## Common Commands

```bash
# Train for 100 generations
python -m flappy_ai.main train --generations 100

# Show neural network visualization
python -m flappy_ai.main train --draw-lines

# Enable debug logging
python -m flappy_ai.main train --log-level DEBUG

# Fast training (no file logging)
python -m flappy_ai.main train --no-log-file
```

## What to Expect

### Generation 1-5
- Birds die quickly
- Score: 0-2 pipes
- Random jumping behavior

### Generation 10-20
- Some birds learn to stay airborne
- Score: 3-10 pipes
- Basic obstacle avoidance

### Generation 30-50
- Consistent performance
- Score: 15-50+ pipes
- Smooth gameplay

## Project Structure (At a Glance)

```
src/flappy_ai/          # Source code
├── main.py             # Run this to train
├── game/               # Game logic
├── ai/                 # NEAT implementation
└── utils/              # Config, logging, helpers

config/                 # NEAT parameters
assets/                 # Game images
checkpoints/            # Saved models
logs/                   # Training logs
```

## Key Files

- `src/flappy_ai/main.py` - Entry point
- `config/config-feedforward.txt` - NEAT parameters
- `src/flappy_ai/utils/config.py` - App configuration
- `checkpoints/winner.pickle` - Best trained model

## Troubleshooting

### Problem: "No module named 'pygame'"
```bash
pip install pygame
```

### Problem: Training is slow
```bash
# Increase simulation speed
python -m flappy_ai.main train --no-log-file
```

### Problem: "FileNotFoundError: Image file not found"
```bash
# Ensure you're in project root
pwd  # Should end with NEAT-Flappy-Bird
ls assets/  # Should show .png files
```

## Configuration

### Game Speed
Edit `src/flappy_ai/utils/config.py`:
```python
FPS: int = 30  # Increase for faster training
```

### Population Size
Edit `config/config-feedforward.txt`:
```
pop_size = 50  # Increase for better results
```

### Window Size
Edit `src/flappy_ai/utils/config.py`:
```python
WIN_WIDTH: int = 600
WIN_HEIGHT: int = 800
```

## Next Steps

1. **Watch Training**: Observe the AI improve over generations
2. **Experiment**: Try different NEAT parameters
3. **Analyze**: Check logs in `logs/` directory
4. **Modify**: Read `docs/ARCHITECTURE.md` to understand the code
5. **Extend**: Add new features or game modes

## Help

- Full documentation: `README.md`
- Architecture details: `docs/ARCHITECTURE.md`
- CLI help: `python -m flappy_ai.main --help`
- Issues: GitHub Issues page

## Performance Tips

| Want to...                | Do this...                           |
|--------------------------|--------------------------------------|
| Train faster             | Use `--no-log-file`, increase FPS    |
| Better AI                | Increase population size, generations|
| See AI thinking          | Use `--draw-lines`                   |
| Debug issues             | Use `--log-level DEBUG`              |
| Save trained model       | Check `checkpoints/winner.pickle`    |

## Example Session

```bash
$ python -m flappy_ai.main train --generations 30
============================================================
NEAT Flappy Bird AI
============================================================
Configuration initialized...
Starting training for 30 generations
============================================================
Starting Generation 1
============================================================
Gen 1: Score reached 1
Gen 1: Score reached 2
Generation 1 completed with score: 2

[...training continues...]

Generation 30 completed with score: 25
Training complete! Best fitness: 152.50
```

Your trained model is saved in `checkpoints/winner.pickle`!
