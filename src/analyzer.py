"""
Analysis module for CORD-19 dataset
"""

import pandas as pd
import numpy as np
from collections import Counter
import re
import logging

logger = logging.getLogger(__name__)

class DataAnalyzer:
    """Class to perform analysis on CORD-19 data"""
    
    def __init__(self, df):
        self.df = df
        
    def analyze_publications_by_year(self):
        """
        Analyze publication trends by year
        
        Returns:
            pd.DataFrame: Publications count by year
        """
        if 'publish_time_year' not in self.df.columns:
            logger.warning("No year column found. Cannot analyze by year.")
            return pd.DataFrame()
        
        yearly_counts = self.df['publish_time_year'].value_counts().sort_index()
        
        result_df = pd.DataFrame({
            'year': yearly_counts.index,
            'publication_count': yearly_counts.values
        })
        
        logger.info(f"Analyzed publications across {len(result_df)} years")
        return result_df
    
    def get_top_journals(self, n=20):
        """
        Get top journals publishing COVID-19 research
        
        Args:
            n (int): Number of top journals to return
            
        Returns:
            pd.DataFrame: Top journals with publication counts
        """
        journal_cols = ['journal', 'source_x']  # Common journal column names
        
        for col in journal_cols:
            if col in self.df.columns:
                journal_counts = self.df[col].value_counts().head(n)
                
                result_df = pd.DataFrame({
                    'journal': journal_counts.index,
                    'publication_count': journal_counts.values
                })
                
                # Remove 'Unknown' entries
                result_df = result_df[result_df['journal'] != 'Unknown']
                
                logger.info(f"Found top {len(result_df)} journals")
                return result_df
        
        logger.warning("No journal column found")
        return pd.DataFrame()
    
    def analyze_title_words(self, n=30, min_length=3):
        """
        Analyze most frequent words in paper titles
        
        Args:
            n (int): Number of top words to return
            min_length (int): Minimum word length to consider
            
        Returns:
            pd.DataFrame: Most frequent words with counts
        """
        if 'title' not in self.df.columns:
            logger.warning("No title column found")
            return pd.DataFrame()
        
        # Combine all titles
        all_titles = ' '.join(self.df['title'].fillna('').astype(str))
        
        # Basic text preprocessing
        # Convert to lowercase and remove punctuation
        all_titles = re.sub(r'[^\w\s]', ' ', all_titles.lower())
        
        # Split into words and filter
        words = [word for word in all_titles.split() 
                if len(word) >= min_length and word not in self._get_stopwords()]
        
        # Count words
        word_counts = Counter(words)
        most_common = word_counts.most_common(n)
        
        result_df = pd.DataFrame(most_common, columns=['word', 'frequency'])
        
        logger.info(f"Analyzed {len(words)} words, returning top {len(result_df)}")
        return result_df
    
    def analyze_source_distribution(self):
        """
        Analyze distribution of papers by source
        
        Returns:
            pd.DataFrame: Source distribution
        """
        source_cols = ['source_x', 'url', 'pmcid']
        
        for col in source_cols:
            if col in self.df.columns and not self.df[col].isna().all():
                # Create source categories
                source_counts = self.df[col].fillna('Unknown').value_counts()
                
                result_df = pd.DataFrame({
                    'source': source_counts.index,
                    'count': source_counts.values
                })
                
                logger.info(f"Analyzed source distribution using column: {col}")
                return result_df
        
        logger.warning("No suitable source column found")
        return pd.DataFrame()
    
    def get_basic_statistics(self):
        """
        Get basic statistics about the dataset
        
        Returns:
            dict: Dictionary of basic statistics
        """
        stats = {
            'total_papers': len(self.df),
            'unique_titles': self.df['title'].nunique() if 'title' in self.df.columns else 0,
            'date_range': None,
            'avg_abstract_length': None,
            'total_journals': 0
        }
        
        # Date range
        if 'publish_time_year' in self.df.columns:
            years = self.df['publish_time_year'].dropna()
            if not years.empty:
                stats['date_range'] = f"{int(years.min())}-{int(years.max())}"
        
        # Average abstract length
        if 'abstract_word_count' in self.df.columns:
            stats['avg_abstract_length'] = round(self.df['abstract_word_count'].mean(), 1)
        
        # Number of unique journals
        journal_cols = ['journal', 'source_x']
        for col in journal_cols:
            if col in self.df.columns:
                stats['total_journals'] = self.df[col].nunique()
                break
        
        return stats
    
    def _get_stopwords(self):
        """
        Get list of common stopwords to exclude from analysis
        
        Returns:
            set: Set of stopwords
        """
        return {
            'the', 'and', 'of', 'in', 'to', 'a', 'is', 'for', 'on', 'with', 
            'as', 'by', 'at', 'an', 'are', 'from', 'or', 'this', 'that', 'be',
            'was', 'will', 'have', 'has', 'been', 'can', 'could', 'would',
            'should', 'may', 'might', 'must', 'shall', 'covid', 'coronavirus',
            'sars', 'cov', '19', '2019', '2020', '2021', '2022', '2023'
        }
    
    def analyze_monthly_trends(self):
        """
        Analyze monthly publication trends
        
        Returns:
            pd.DataFrame: Monthly publication counts
        """
        if 'publish_time_month' not in self.df.columns:
            logger.warning("No month column found")
            return pd.DataFrame()
        
        monthly_counts = self.df['publish_time_month'].value_counts().sort_index()
        
        month_names = {
            1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
            7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
        }
        
        result_df = pd.DataFrame({
            'month': [month_names.get(m, str(m)) for m in monthly_counts.index],
            'publication_count': monthly_counts.values
        })
        
        return result_df