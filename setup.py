"""
Setup configuration for NEAT Flappy Bird AI package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = (this_directory / "requirements.txt").read_text().strip().split("\n")

setup(
    name="flappy-ai",
    version="1.0.0",
    author="Tech With Tim (Refactored)",
    author_email="",
    description="A production-ready NEAT algorithm implementation for training AI to play Flappy Bird",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/NEAT-Flappy-Bird",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/NEAT-Flappy-Bird/issues",
        "Source": "https://github.com/yourusername/NEAT-Flappy-Bird",
        "Documentation": "https://github.com/yourusername/NEAT-Flappy-Bird/blob/master/README.md",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Games/Entertainment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "isort>=5.12.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "flappy-ai=flappy_ai.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md"],
    },
    keywords="neat neural-network ai machine-learning game flappy-bird reinforcement-learning",
    zip_safe=False,
)
