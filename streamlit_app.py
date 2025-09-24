"""
Streamlit Application for CORD-19 Data Explorer
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Add src directory to path
sys.path.append('src')

from data_loader import DataLoader
from data_cleaner import DataCleaner
from analyzer import DataAnalyzer
from visualizer import DataVisualizer

# Page configuration
st.set_page_config(
    page_title="CORD-19 Data Explorer",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
</style>
""", unsafe_allow_html=True)

# Cache data loading functions
@st.cache_data
def load_and_process_data():
    """Load and process the CORD-19 data"""
    try:
        # Try to load cleaned data first
        if os.path.exists('data/cleaned_metadata.csv'):
            df = pd.read_csv('data/cleaned_metadata.csv')
            st.success("✅ Loaded pre-processed data")
        else:
            # Load and clean raw data
            loader = DataLoader('data/metadata.csv')
            df = loader.load_data(sample_size=10000)  # Use sample for demo
            
            cleaner = DataCleaner(df)
            df = cleaner.get_cleaned_data()
            st.success("✅ Data loaded and processed successfully")
        
        return df
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None

@st.cache_data
def get_analysis_data(df):
    """Get all analysis results"""
    analyzer = DataAnalyzer(df)
    
    return {
        'basic_stats': analyzer.get_basic_statistics(),
        'yearly_data': analyzer.analyze_publications_by_year(),
        'journal_data': analyzer.get_top_journals(20),
        'word_data': analyzer.analyze_title_words(50),
        'source_data': analyzer.analyze_source_distribution(),
        'monthly_data': analyzer.analyze_monthly_trends()
    }

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">🦠 CORD-19 Data Explorer</h1>', unsafe_allow_html=True)
    st.markdown("**Exploring COVID-19 Research Papers Dataset**")
    st.markdown("---")
    
    # Load data
    with st.spinner("Loading and processing data..."):
        df = load_and_process_data()
    
    if df is None:
        st.error("Please ensure the data file is in the 'data' folder")
        st.stop()
    
    # Get analysis data
    with st.spinner("Performing analysis..."):
        analysis_data = get_analysis_data(df)
    
    # Sidebar controls
    st.sidebar.title("🔧 Controls")
    st.sidebar.markdown("---")
    
    # Year filter
    if 'publish_time_year' in df.columns:
        years = sorted(df['publish_time_year'].dropna().unique())
        if len(years) > 1:
            year_range = st.sidebar.slider(
                "Select Year Range",
                min_value=int(min(years)),
                max_value=int(max(years)),
                value=(int(min(years)), int(max(years))),
                step=1
            )
            
            # Filter data based on year selection
            mask = (df['publish_time_year'] >= year_range[0]) & (df['publish_time_year'] <= year_range[1])
            df_filtered = df[mask]
        else:
            df_filtered = df
            year_range = None
    else:
        df_filtered = df
        year_range = None
    
    # Number of journals to show
    n_journals = st.sidebar.selectbox(
        "Number of Top Journals to Show",
        [5, 10, 15, 20],
        index=2
    )
    
    # Word cloud options
    n_words = st.sidebar.selectbox(
        "Number of Words in Word Cloud",
        [20, 30, 50, 100],
        index=1
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("💡 Use the controls above to customize the visualizations")
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", "📈 Publication Trends", "🏛️ Top Journals", 
        "☁️ Word Analysis", "📋 Raw Data"
    ])
    
    # Tab 1: Overview
    with tab1:
        st.header("Dataset Overview")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(
                f'<div class="metric-card"><h3>{len(df_filtered):,}</h3><p>Total Papers</p></div>',
                unsafe_allow_html=True
            )
        
        with col2:
            unique_titles = df_filtered['title'].nunique() if 'title' in df_filtered.columns else 0
            st.markdown(
                f'<div class="metric-card"><h3>{unique_titles:,}</h3><p>Unique Titles</p></div>',
                unsafe_allow_html=True
            )
        
        with col3:
            if 'publish_time_year' in df_filtered.columns:
                years_span = f"{df_filtered['publish_time_year'].min():.0f}-{df_filtered['publish_time_year'].max():.0f}"
            else:
                years_span = "N/A"
            st.markdown(
                f'<div class="metric-card"><h3>{years_span}</h3><p>Year Range</p></div>',
                unsafe_allow_html=True
            )
        
        with col4:
            avg_abstract = analysis_data['basic_stats'].get('avg_abstract_length', 0)
            st.markdown(
                f'<div class="metric-card"><h3>{avg_abstract:.0f}</h3><p>Avg Abstract Length</p></div>',
                unsafe_allow_html=True
            )
        
        st.markdown("---")
        
        # Quick insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(" Quick Insights")
            
            yearly_data = analysis_data['yearly_data']
            if not yearly_data.empty and year_range:
                yearly_filtered = yearly_data[
                    (yearly_data['year'] >= year_range[0]) & 
                    (yearly_data['year'] <= year_range[1])
                ]
                
                if not yearly_filtered.empty:
                    peak_year = yearly_filtered.loc[yearly_filtered['publication_count'].idxmax()]
                    st.write(f" **Peak Publication Year:** {peak_year['year']} ({peak_year['publication_count']:,} papers)")
                    
                    total_papers = yearly_filtered['publication_count'].sum()
                    st.write(f" **Total Papers in Range:** {total_papers:,}")
                    
                    growth_rate = ((yearly_filtered['publication_count'].iloc[-1] - yearly_filtered['publication_count'].iloc[0]) / yearly_filtered['publication_count'].iloc[0] * 100) if len(yearly_filtered) > 1 else 0
                    st.write(f" **Growth Rate:** {growth_rate:.1f}%")
        
        with col2:
            st.subheader("🔍 Data Quality")
            
            total_columns = len(df_filtered.columns)
            complete_columns = (df_filtered.isnull().sum() == 0).sum()
            completeness = complete_columns / total_columns * 100
            
            st.write(f" **Total Columns:** {total_columns}")
            st.write(f" **Complete Columns:** {complete_columns}")
            st.write(f" **Data Completeness:** {completeness:.1f}%")
            
            # Memory usage
            memory_mb = df_filtered.memory_usage(deep=True).sum() / 1024**2
            st.write(f" **Memory Usage:** {memory_mb:.2f} MB")
    
    # Tab 2: Publication Trends
    with tab2:
        st.header("Publication Trends Over Time")
        
        yearly_data = analysis_data['yearly_data']
        if not yearly_data.empty:
            if year_range:
                yearly_filtered = yearly_data[
                    (yearly_data['year'] >= year_range[0]) & 
                    (yearly_data['year'] <= year_range[1])
                ]
            else:
                yearly_filtered = yearly_data
            
            # Interactive plot using Plotly
            fig = px.line(
                yearly_filtered, 
                x='year', 
                y='publication_count',
                title=f'COVID-19 Research Publications Over Time {f"({year_range[0]}-{year_range[1]})" if year_range else ""}',
                markers=True,
                line_shape='spline'
            )
            
            fig.update_traces(
                line=dict(width=3),
                marker=dict(size=8),
                hovertemplate='<b>Year:</b> %{x}<br><b>Publications:</b> %{y:,}<extra></extra>'
            )
            
            fig.update_layout(
                height=500,
                xaxis_title="Year",
                yaxis_title="Number of Publications",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show data table
            with st.expander(" View Data Table"):
                st.dataframe(yearly_filtered, use_container_width=True)
        else:
            st.warning("No yearly publication data available")
        
        # Monthly trends if available
        monthly_data = analysis_data['monthly_data']
        if not monthly_data.empty:
            st.subheader("Monthly Publication Patterns")
            
            fig_monthly = px.bar(
                monthly_data,
                x='month',
                y='publication_count',
                title='Publication Distribution by Month',
                color='publication_count',
                color_continuous_scale='viridis'
            )
            
            fig_monthly.update_layout(height=400)
            st.plotly_chart(fig_monthly, use_container_width=True)
    
    # Tab 3: Top Journals
    with tab3:
        st.header("Top Journals Publishing COVID-19 Research")
        
        journal_data = analysis_data['journal_data']
        if not journal_data.empty:
            # Filter based on user selection
            top_journals = journal_data.head(n_journals)
            
            # Interactive bar chart
            fig = px.bar(
                top_journals,
                y='journal',
                x='publication_count',
                orientation='h',
                title=f'Top {n_journals} Journals by Publication Count',
                color='publication_count',
                color_continuous_scale='plasma'
            )
            
            fig.update_layout(
                height=max(400, n_journals * 30),
                yaxis=dict(tickmode='linear'),
                xaxis_title="Number of Publications",
                yaxis_title="Journal"
            )
            
            fig.update_traces(
                hovertemplate='<b>%{y}</b><br>Publications: %{x:,}<extra></extra>'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show data table
            with st.expander(" View Journal Data"):
                st.dataframe(top_journals, use_container_width=True)
        else:
            st.warning("No journal data available")
    
    # Tab 4: Word Analysis
    with tab4:
        st.header("Word Frequency Analysis")
        
        word_data = analysis_data['word_data']
        if not word_data.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Word Cloud")
                
                # Create word cloud using matplotlib (since plotly doesn't have native word cloud)
                try:
                    from wordcloud import WordCloud
                    
                    word_freq = dict(zip(word_data['word'][:n_words], word_data['frequency'][:n_words]))
                    
                    wordcloud = WordCloud(
                        width=400, height=300,
                        background_color='white',
                        colormap='viridis',
                        max_words=n_words
                    ).generate_from_frequencies(word_freq)
                    
                    fig_wc, ax = plt.subplots(figsize=(8, 6))
                    ax.imshow(wordcloud, interpolation='bilinear')
                    ax.axis('off')
                    ax.set_title('Most Frequent Words in Paper Titles', fontsize=14, fontweight='bold')
                    
                    st.pyplot(fig_wc)
                    
                except ImportError:
                    st.error("WordCloud library not available. Please install it: pip install wordcloud")
            
            with col2:
                st.subheader("Top Words")
                
                # Bar chart of top words
                top_words = word_data.head(n_words)
                
                fig_words = px.bar(
                    top_words,
                    x='frequency',
                    y='word',
                    orientation='h',
                    title=f'Top {min(n_words, len(top_words))} Most Frequent Words',
                    color='frequency',
                    color_continuous_scale='blues'
                )
                
                fig_words.update_layout(
                    height=max(400, len(top_words) * 20),
                    yaxis=dict(categoryorder='total ascending'),
                    xaxis_title="Frequency",
                    yaxis_title="Word"
                )
                
                st.plotly_chart(fig_words, use_container_width=True)
            
            # Show word frequency table
            with st.expander("📊 View Word Frequency Data"):
                st.dataframe(word_data.head(50), use_container_width=True)
        else:
            st.warning("No word frequency data available")
    
    # Tab 5: Raw Data
    with tab5:
        st.header("Raw Dataset")
        
        # Data filtering options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            show_columns = st.multiselect(
                "Select Columns to Display",
                options=list(df_filtered.columns),
                default=list(df_filtered.columns)[:5]  # Show first 5 columns by default
            )
        
        with col2:
            n_rows = st.selectbox(
                "Number of Rows to Display",
                [10, 25, 50, 100, 500],
                index=2
            )
        
        with col3:
            search_term = st.text_input(
                "Search in Titles",
                placeholder="Enter search term..."
            )
        
        # Apply filters
        display_df = df_filtered.copy()
        
        if show_columns:
            display_df = display_df[show_columns]
        
        if search_term and 'title' in display_df.columns:
            mask = display_df['title'].str.contains(search_term, case=False, na=False)
            display_df = display_df[mask]
            st.info(f"Found {len(display_df)} papers containing '{search_term}'")
        
        # Display data
        st.dataframe(
            display_df.head(n_rows),
            use_container_width=True,
            height=400
        )
        
        # Download options
        st.subheader("Download Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Download filtered data as CSV
            csv = display_df.to_csv(index=False)
            st.download_button(
                label=" Download Filtered Data as CSV",
                data=csv,
                file_name=f"cord19_filtered_data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Download analysis results
            if not analysis_data['yearly_data'].empty:
                yearly_csv = analysis_data['yearly_data'].to_csv(index=False)
                st.download_button(
                    label=" Download Analysis Results",
                    data=yearly_csv,
                    file_name=f"cord19_yearly_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(" **Data Source:** CORD-19 Dataset from Kaggle")
    
    with col2:
        st.info(" **Built with:** Python, Streamlit, Pandas, Plotly")
    
    with col3:
        st.info(" **Last Updated:** " + datetime.now().strftime("%Y-%m-%d"))
    
    # Sidebar additional info
    with st.sidebar:
        st.markdown("---")
        st.subheader("ℹ About")
        st.markdown("""
        This application provides an interactive exploration of the CORD-19 dataset,
        which contains research papers about COVID-19 and related coronavirus research.
        
        **Features:**
        -  Interactive visualizations
        -  Data filtering and search
        -  Publication trend analysis
        -  Top journals identification
        -  Word frequency analysis
        -  Data download capabilities
        """)
        
        st.markdown("---")
        st.markdown("**Navigation Tips:**")
        st.markdown("- Use the year slider to filter data")
        st.markdown("- Hover over charts for details")
        st.markdown("- Click legend items to toggle series")
        st.markdown("- Use tabs to explore different aspects")

if __name__ == "__main__":
    main()