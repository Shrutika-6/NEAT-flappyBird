"""Allow running the package as a module with python -m flappy_ai"""

from .main import main
import sys

if __name__ == "__main__":
    sys.exit(main())
