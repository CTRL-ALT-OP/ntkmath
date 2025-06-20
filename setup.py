"""
Setup script for ntkmath package.
"""

from setuptools import setup, find_packages

# Read the contents of README file (if it exists)
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "A collection of mathematical utility functions and classes."

setup(
    name="ntkmath",
    version="0.1.0",
    author="CTRL-ALT-OP",
    description="A collection of mathematical utility functions and classes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ntkmath",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        # Add any external dependencies here
        # For example: "numpy>=1.20.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black",
            "isort",
            "flake8",
        ],
    },
    keywords="math mathematics utilities algebra geometry statistics",
)
