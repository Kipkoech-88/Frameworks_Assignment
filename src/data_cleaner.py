"""
Data cleaning module for CORD-19 dataset analysis
"""

import pandas as pd
import numpy as np
import re
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DataCleaner:
    """Class to handle data cleaning and preparation"""
    
    def __init__(self, df):
        self.df = df.copy()
        self.cleaned_df = None
        
    def handle_missing_values(self, strategy='drop_high_missing'):
        """
        Handle missing values in the dataset
        
        Args:
            strategy (str): Strategy to handle missing values
                          'drop_high_missing' - drop columns with >70% missing
                          'fill' - fill with appropriate values
        """
        logger.info("Handling missing values...")
        
        if strategy == 'drop_high_missing':
            # Calculate missing percentage for each column
            missing_pct = (self.df.isnull().sum() / len(self.df) * 100)
            
            # Drop columns with more than 70% missing values
            cols_to_drop = missing_pct[missing_pct > 70].index.tolist()
            logger.info(f"Dropping columns with >70% missing: {cols_to_drop}")
            
            self.df = self.df.drop(columns=cols_to_drop)
        
        # Fill remaining missing values strategically
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                # Fill text columns with 'Unknown'
                self.df[col].fillna('Unknown', inplace=True)
            elif self.df[col].dtype in ['int64', 'float64']:
                # Fill numerical columns with median
                self.df[col].fillna(self.df[col].median(), inplace=True)
        
        logger.info("Missing values handled")
        
    def prepare_dates(self, date_columns=['publish_time']):
        """
        Convert date columns to datetime and extract useful features
        
        Args:
            date_columns (list): List of columns to convert to datetime
        """
        logger.info("Preparing date columns...")
        
        for col in date_columns:
            if col in self.df.columns:
                try:
                    # Convert to datetime, handling various formats
                    self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                    
                    # Extract year for analysis
                    year_col = f"{col}_year"
                    self.df[year_col] = self.df[col].dt.year
                    
                    # Extract month for seasonal analysis
                    month_col = f"{col}_month"
                    self.df[month_col] = self.df[col].dt.month
                    
                    logger.info(f"Processed date column: {col}")
                    
                except Exception as e:
                    logger.warning(f"Could not process date column {col}: {str(e)}")
    
    def create_text_features(self):
        """
        Create additional features from text columns
        """
        logger.info("Creating text features...")
        
        # Abstract word count
        if 'abstract' in self.df.columns:
            self.df['abstract_word_count'] = self.df['abstract'].apply(
                lambda x: len(str(x).split()) if pd.notna(x) else 0
            )
        
        # Title word count
        if 'title' in self.df.columns:
            self.df['title_word_count'] = self.df['title'].apply(
                lambda x: len(str(x).split()) if pd.notna(x) else 0
            )
        
        # Number of authors (if authors column exists)
        if 'authors' in self.df.columns:
            self.df['author_count'] = self.df['authors'].apply(
                lambda x: len(str(x).split(';')) if pd.notna(x) and str(x) != 'Unknown' else 0
            )
        
        logger.info("Text features created")
    
    def clean_text_columns(self, text_columns=['title', 'abstract']):
        """
        Basic cleaning of text columns
        
        Args:
            text_columns (list): List of text columns to clean
        """
        logger.info("Cleaning text columns...")
        
        for col in text_columns:
            if col in self.df.columns:
                # Remove extra whitespace and normalize
                self.df[col] = self.df[col].apply(
                    lambda x: ' '.join(str(x).split()) if pd.notna(x) else ''
                )
                
                # Remove non-printable characters
                self.df[col] = self.df[col].apply(
                    lambda x: re.sub(r'[^\x20-\x7E]', '', str(x))
                )
        
        logger.info("Text columns cleaned")
    
    def filter_data(self, year_range=(2019, 2023)):
        """
        Filter data based on criteria
        
        Args:
            year_range (tuple): Year range to keep (start_year, end_year)
        """
        logger.info(f"Filtering data for years {year_range[0]}-{year_range[1]}")
        
        # Filter by year if publish_time_year exists
        if 'publish_time_year' in self.df.columns:
            initial_count = len(self.df)
            self.df = self.df[
                (self.df['publish_time_year'] >= year_range[0]) & 
                (self.df['publish_time_year'] <= year_range[1])
            ]
            final_count = len(self.df)
            logger.info(f"Filtered from {initial_count} to {final_count} rows")
        
        # Remove rows with empty titles
        if 'title' in self.df.columns:
            initial_count = len(self.df)
            self.df = self.df[
                (self.df['title'].notna()) & 
                (self.df['title'] != '') & 
                (self.df['title'] != 'Unknown')
            ]
            final_count = len(self.df)
            logger.info(f"Removed empty titles: {initial_count} to {final_count} rows")
    
    def get_cleaned_data(self):
        """
        Apply all cleaning steps and return cleaned dataframe
        
        Returns:
            pd.DataFrame: Cleaned dataframe
        """
        logger.info("Starting comprehensive data cleaning...")
        
        # Apply all cleaning steps
        self.handle_missing_values()
        self.prepare_dates()
        self.create_text_features()
        self.clean_text_columns()
        self.filter_data()
        
        self.cleaned_df = self.df.copy()
        
        logger.info(f"Data cleaning completed. Final shape: {self.cleaned_df.shape}")
        
        return self.cleaned_df