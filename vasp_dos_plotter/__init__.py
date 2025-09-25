"""
VASP DOS Plotter - A professional GUI application for plotting VASP Density of States data.

This package provides tools for visualizing and analyzing Density of States (DOS)
data from VASP (Vienna Ab initio Simulation Package) calculations.

Main components:
- DOSPlotterGUI: The main GUI application
- plot_real_dos: Command-line plotting functionality

Author: Zeinab H. Fard
Email: zfard@iastate.edu
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Zeinab H. Fard"
__email__ = "zfard@iastate.edu"
__license__ = "MIT"

from .gui import DOSPlotterGUI
from .plotter import plot_dos_file

__all__ = ["DOSPlotterGUI", "plot_dos_file", "__version__"]
