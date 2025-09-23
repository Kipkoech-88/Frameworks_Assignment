"""
Data loading module for CORD-19 dataset analysis
"""

import pandas as pd
import numpy as np
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    """Class to handle loading and basic exploration of CORD-19 metadata"""
    
    def __init__(self, data_path="data/metadata.csv"):
        self.data_path = data_path
        self.df = None
        
    def load_data(self, sample_size=None):
        """
        Load the CORD-19 metadata CSV file
        
        Args:
            sample_size (int): If specified, load only a sample of this size
        
        Returns:
            pd.DataFrame: Loaded dataframe
        """
        try:
            if not os.path.exists(self.data_path):
                raise FileNotFoundError(f"Data file not found: {self.data_path}")
            
            logger.info(f"Loading data from {self.data_path}")
            
            # Load data with error handling for large files
            if sample_size:
                self.df = pd.read_csv(self.data_path, nrows=sample_size)
                logger.info(f"Loaded sample of {sample_size} rows")
            else:
                self.df = pd.read_csv(self.data_path)
                logger.info(f"Loaded full dataset")
            
            return self.df
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def basic_exploration(self):
        """
        Perform basic exploration of the loaded dataset
        
        Returns:
            dict: Dictionary containing exploration results
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        exploration_results = {
            'shape': self.df.shape,
            'columns': list(self.df.columns),
            'dtypes': self.df.dtypes.to_dict(),
            'missing_values': self.df.isnull().sum().to_dict(),
            'memory_usage': self.df.memory_usage(deep=True).sum() / 1024**2,  # MB
        }
        
        # Basic statistics for numerical columns
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) > 0:
            exploration_results['numerical_stats'] = self.df[numerical_cols].describe().to_dict()
        
        logger.info(f"Dataset shape: {exploration_results['shape']}")
        logger.info(f"Memory usage: {exploration_results['memory_usage']:.2f} MB")
        
        return exploration_results
    
    def display_sample(self, n=5):
        """
        Display first n rows of the dataset
        
        Args:
            n (int): Number of rows to display
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        return self.df.head(n)
    
    def get_column_info(self):
        """
        Get detailed information about each column
        
        Returns:
            pd.DataFrame: Information about columns
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        column_info = pd.DataFrame({
            'Column': self.df.columns,
            'Non-Null Count': self.df.count(),
            'Null Count': self.df.isnull().sum(),
            'Null Percentage': (self.df.isnull().sum() / len(self.df) * 100).round(2),
            'Data Type': self.df.dtypes
        })
        
        return column_info.reset_index(drop=True)