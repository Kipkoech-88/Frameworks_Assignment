"""
CORD-19 Data Analysis Package

This package provides tools for loading, cleaning, analyzing, and visualizing
the CORD-19 research dataset.

Modules:
    data_loader: Load and explore CORD-19 data
    data_cleaner: Clean and preprocess data
    analyzer: Perform statistical analysis
    visualizer: Create visualizations
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .data_loader import DataLoader
from .data_cleaner import DataCleaner
from .analyzer import DataAnalyzer
from .visualizer import DataVisualizer

__all__ = ['DataLoader', 'DataCleaner', 'DataAnalyzer', 'DataVisualizer']