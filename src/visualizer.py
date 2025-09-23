"""
Visualization module for CORD-19 dataset analysis
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
import logging

logger = logging.getLogger(__name__)

# Set style
plt.style.use('default')
sns.set_palette("husl")

class DataVisualizer:
    """Class to create visualizations for CORD-19 analysis"""
    
    def __init__(self):
        self.fig_size = (12, 6)
        
    def plot_publications_by_year(self, year_data, title="COVID-19 Research Publications by Year"):
        """
        Create a line plot of publications by year
        
        Args:
            year_data (pd.DataFrame): DataFrame with 'year' and 'publication_count' columns
            title (str): Plot title
            
        Returns:
            matplotlib.figure.Figure: The figure object
        """
        fig, ax = plt.subplots(figsize=self.fig_size)
        
        if not year_data.empty:
            ax.plot(year_data['year'], year_data['publication_count'], 
                   marker='o', linewidth=3, markersize=8)
            ax.fill_between(year_data['year'], year_data['publication_count'], 
                           alpha=0.3)
            
            # Annotations for peak values
            max_idx = year_data['publication_count'].idxmax()
            max_year = year_data.loc[max_idx, 'year']
            max_count = year_data.loc[max_idx, 'publication_count']
            
            ax.annotate(f'Peak: {max_count:,} papers', 
                       xy=(max_year, max_count), 
                       xytext=(10, 10), textcoords='offset points',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                       arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Publications', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Format y-axis with commas
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
        
        plt.tight_layout()
        return fig
    
    def plot_top_journals(self, journal_data, title="Top Journals Publishing COVID-19 Research", n=15):
        """
        Create a horizontal bar chart of top journals
        
        Args:
            journal_data (pd.DataFrame): DataFrame with 'journal' and 'publication_count' columns
            title (str): Plot title
            n (int): Number of journals to display
            
        Returns:
            matplotlib.figure.Figure: The figure object
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        
        if not journal_data.empty:
            # Take top n journals
            top_journals = journal_data.head(n)
            
            # Create horizontal bar chart
            bars = ax.barh(range(len(top_journals)), top_journals['publication_count'])
            
            # Color bars with gradient
            colors = plt.cm.viridis(np.linspace(0, 1, len(bars)))
            for bar, color in zip(bars, colors):
                bar.set_color(color)
            
            # Set labels
            ax.set_yticks(range(len(top_journals)))
            ax.set_yticklabels([j[:50] + '...' if len(j) > 50 else j 
                               for j in top_journals['journal']], fontsize=10)
            
            # Add value labels on bars
            for i, (bar, count) in enumerate(zip(bars, top_journals['publication_count'])):
                ax.text(bar.get_width() + max(top_journals['publication_count']) * 0.01, 
                       bar.get_y() + bar.get_height()/2, f'{count:,}',
                       va='center', fontweight='bold')
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Number of Publications', fontsize=12, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_word_cloud(self, word_data, title="Most Frequent Words in Paper Titles"):
        """
        Create a word cloud from word frequency data
        
        Args:
            word_data (pd.DataFrame): DataFrame with 'word' and 'frequency' columns
            title (str): Plot title
            
        Returns:
            matplotlib.figure.Figure: The figure object
        """
        fig, ax = plt.subplots(figsize=self.fig_size)
        
        if not word_data.empty:
            # Create word frequency dictionary
            word_freq = dict(zip(word_data['word'], word_data['frequency']))
            
            # Generate word cloud
            wordcloud = WordCloud(
                width=800, height=400, 
                background_color='white',
                colormap='viridis',
                max_words=100,
                relative_scaling=0.5
            ).generate_from_frequencies(word_freq)
            
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
        else:
            ax.text(0.5, 0.5, 'No word data available', 
                   transform=ax.transAxes, ha='center', va='center',
                   fontsize=16)
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        return fig
    
    def plot_source_distribution(self, source_data, title="Distribution of Papers by Source"):
        """
        Create a pie chart of source distribution
        
        Args:
            source_data (pd.DataFrame): DataFrame with 'source' and 'count' columns
            title (str): Plot title
            
        Returns:
            matplotlib.figure.Figure: The figure object
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        if not source_data.empty:
            # Take top 10 sources and group others
            top_sources = source_data.head(10)
            other_count = source_data.iloc[10:]['count'].sum() if len(source_data) > 10 else 0
            
            if other_count > 0:
                plot_data = pd.concat([
                    top_sources,
                    pd.DataFrame({'source': ['Others'], 'count': [other_count]})
                ])
            else:
                plot_data = top_sources
            
            # Create pie chart
            wedges, texts, autotexts = ax.pie(
                plot_data['count'], 
                labels=[s[:20] + '...' if len(s) > 20 else s for s in plot_data['source']],
                autopct='%1.1f%%',
                startangle=90
            )
            
            # Enhance text
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        return fig
    
    def plot_monthly_trends(self, monthly_data, title="Monthly Publication Trends"):
        """
        Create a bar chart of monthly trends
        
        Args:
            monthly_data (pd.DataFrame): DataFrame with 'month' and 'publication_count' columns
            title (str): Plot title
            
        Returns:
            matplotlib.figure.Figure: The figure object
        """
        fig, ax = plt.subplots(figsize=self.fig_size)
        
        if not monthly_data.empty:
            bars = ax.bar(monthly_data['month'], monthly_data['publication_count'])
            
            # Color bars with gradient
            colors = plt.cm.coolwarm(np.linspace(0, 1, len(bars)))
            for bar, color in zip(bars, colors):
                bar.set_color(color)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                       f'{int(height):,}', ha='center', va='bottom', fontweight='bold')
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Month', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Publications', fontsize=12, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig
    
    def create_interactive_timeline(self, year_data):
        """
        Create an interactive plotly timeline
        
        Args:
            year_data (pd.DataFrame): DataFrame with 'year' and 'publication_count' columns
            
        Returns:
            plotly.graph_objects.Figure: Interactive figure
        """
        if year_data.empty:
            return go.Figure()
        
        fig = px.line(year_data, x='year', y='publication_count',
                      title='Interactive COVID-19 Research Timeline',
                      markers=True, line_shape='spline')
        
        fig.update_layout(
            title_font_size=16,
            xaxis_title="Year",
            yaxis_title="Number of Publications",
            hovermode='x unified'
        )
        
        fig.update_traces(
            hovertemplate='<b>Year:</b> %{x}<br><b>Publications:</b> %{y:,}<extra></extra>',
            line=dict(width=3),
            marker=dict(size=8)
        )
        
        return fig
    
    def create_summary_dashboard(self, stats_dict):
        """
        Create a summary statistics visualization
        
        Args:
            stats_dict (dict): Dictionary of basic statistics
            
        Returns:
            matplotlib.figure.Figure: The figure object
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Total papers
        ax1.text(0.5, 0.5, f"{stats_dict['total_papers']:,}", 
                transform=ax1.transAxes, ha='center', va='center',
                fontsize=36, fontweight='bold', color='navy')
        ax1.text(0.5, 0.2, 'Total Papers', 
                transform=ax1.transAxes, ha='center', va='center',
                fontsize=14, fontweight='bold')
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, 1)
        ax1.axis('off')
        
        # Date range
        ax2.text(0.5, 0.5, str(stats_dict.get('date_range', 'N/A')), 
                transform=ax2.transAxes, ha='center', va='center',
                fontsize=24, fontweight='bold', color='darkgreen')
        ax2.text(0.5, 0.2, 'Date Range', 
                transform=ax2.transAxes, ha='center', va='center',
                fontsize=14, fontweight='bold')
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0, 1)
        ax2.axis('off')
        
        # Unique titles
        ax3.text(0.5, 0.5, f"{stats_dict['unique_titles']:,}", 
                transform=ax3.transAxes, ha='center', va='center',
                fontsize=36, fontweight='bold', color='purple')
        ax3.text(0.5, 0.2, 'Unique Titles', 
                transform=ax3.transAxes, ha='center', va='center',
                fontsize=14, fontweight='bold')
        ax3.set_xlim(0, 1)
        ax3.set_ylim(0, 1)
        ax3.axis('off')
        
        # Average abstract length
        avg_length = stats_dict.get('avg_abstract_length', 0)
        ax4.text(0.5, 0.5, f"{avg_length:.0f}" if avg_length else 'N/A', 
                transform=ax4.transAxes, ha='center', va='center',
                fontsize=36, fontweight='bold', color='darkorange')
        ax4.text(0.5, 0.2, 'Avg Abstract Length', 
                transform=ax4.transAxes, ha='center', va='center',
                fontsize=14, fontweight='bold')
        ax4.set_xlim(0, 1)
        ax4.set_ylim(0, 1)
        ax4.axis('off')
        
        plt.suptitle('CORD-19 Dataset Summary', fontsize=20, fontweight='bold', y=0.95)
        plt.tight_layout()
        return fig