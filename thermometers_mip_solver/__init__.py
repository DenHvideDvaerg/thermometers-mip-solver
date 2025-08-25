"""
Thermometers MIP Solver -  Mixed Integer Programming approach to solving Thermometers logic puzzles.
"""

from .puzzle import Thermometer, ThermometerPuzzle
from .solver import ThermometersSolver

__version__ = "0.1.1"
__all__ = ["Thermometer", "ThermometerPuzzle", "ThermometersSolver"]
