"""
ntkmath - A collection of mathematical utility functions and classes.
"""

# Import all public functions and classes from submodules
from .general import Curves, clamp, sign
from .geometry import (
    Rectangle,
    Triangle,
    Angle,
    Point,
    Line,
)
from .adv_decimal import FixedPointArithmetic, FPT, Decimal

# This list controls what gets imported with "from ntkmath import *"
__all__ = [
    # General utilities
    "Curves",
    "clamp",
    "sign",
    # Geometry classes and functions
    "Rectangle",
    "Triangle",
    "Angle",
    "Point",
    "Line",
    # Advanced decimal arithmetic
    "FixedPointArithmetic",
    "FPT",
    "Decimal",
]
