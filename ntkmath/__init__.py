"""
ntkmath - A collection of mathematical utility functions and classes.
"""

# Import all public functions and classes from submodules
# This allows users to do: from ntkmath import function_name

# Algebra module
from .algebra import solve_quadratic, LinearEquation

# Geometry module
from .geometry import Point, Circle, distance

# Statistics module
from .statistics import mean, median, mode, std_dev, variance

# This list controls what gets imported with "from ntkmath import *"
__all__ = []
