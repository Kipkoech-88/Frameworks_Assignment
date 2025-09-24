# CORD-19 Data Explorer

## 🦠 COVID-19 Research Papers Analysis

This project provides a comprehensive analysis of the CORD-19 dataset, which contains research papers about COVID-19 and related coronavirus research. The project includes data exploration, cleaning, analysis, and an interactive Streamlit web application for visualizing insights.

## 📁 Project Structure

```
Frameworks_Assignment/
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
├── streamlit_app.py           # Main Streamlit application
├── data/                      # Data directory
│   ├── metadata.csv          # Original CORD-19 metadata (download required)
│   └── cleaned_metadata.csv  # Processed data (generated)
├── src/                      # Source code modules
│   ├── __init__.py
│   ├── data_loader.py        # Data loading functionality
│   ├── data_cleaner.py       # Data cleaning and preprocessing
│   ├── analyzer.py           # Data analysis functions
│   └── visualizer.py         # Visualization utilities
├── notebooks/                # Jupyter notebooks
│   └── data_exploration.ipynb # Exploratory data analysis
└── results/                  # Analysis results
    ├── findings_report.md    # Key findings summary
    ├── yearly_publications.csv
    ├── top_journals.csv
    └── word_frequency.csv
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Frameworks_Assignment.git
cd Frameworks_Assignment
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download the Dataset

1. Go to [CORD-19 Dataset on Kaggle](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge)
2. Download the `metadata.csv` file
3. Place it in the `data/` directory

### 4. Run the Analysis

#### Option A: Jupyter Notebook (Recommended for exploration)

```bash
jupyter notebook notebooks/data_exploration.ipynb
```

#### Option B: Streamlit App (Interactive web interface)

```bash
streamlit run streamlit_app.py
```

The Streamlit app will open in your browser at `http://localhost:8501`

## 📊 Features

### Data Processing
- **Automated Data Loading**: Handles large CSV files with error management
- **Intelligent Cleaning**: Removes high-missing columns, handles missing values
- **Feature Engineering**: Creates date features, text statistics, author counts
- **Data Validation**: Ensures data quality and consistency

### Analysis Capabilities
- **Publication Trends**: Time series analysis of research output
- **Journal Analysis**: Identification of top publishing journals
- **Text Mining**: Word frequency analysis and keyword extraction
- **Source Distribution**: Analysis of data sources and repositories
- **Statistical Summaries**: Comprehensive dataset statistics

### Visualizations
- **Interactive Charts**: Plotly-based interactive visualizations
- **Word Clouds**: Visual representation of frequent terms
- **Time Series Plots**: Publication trends over time
- **Bar Charts**: Top journals and word frequencies
- **Distribution Plots**: Source and categorical data analysis

### Web Application
- **Interactive Dashboard**: Real-time data exploration
- **Filtering Controls**: Year range, journal count, word limits
- **Multiple Views**: Overview, trends, journals, words, raw data
- **Data Export**: Download filtered data and analysis results
- **Responsive Design**: Works on desktop and mobile devices

## 🔧 Configuration

### Data Sampling
For large datasets, you can use sampling in the data loader:

```python
# In data_loader.py or notebooks
df = loader.load_data(sample_size=50000)  # Use 50k rows for testing
```

### Streamlit Configuration
Modify `streamlit_app.py` for custom settings:

```python
# Page configuration
st.set_page_config(
    page_title="Your Custom Title",
    page_icon="🔬",
    layout="wide"
)
```

## 📈 Analysis Results

The analysis provides insights into:

1. **Publication Volume**: Total research papers and growth trends
2. **Temporal Patterns**: Peak publication periods and seasonal variations
3. **Research Focus**: Most common keywords and research themes
4. **Publication Venues**: Leading journals and conferences
5. **Data Sources**: Distribution across different repositories

## 🛠️ Technical Implementation

### Data Processing Pipeline
1. **Loading**: CSV parsing with pandas, memory optimization
2. **Cleaning**: Missing value handling, data type conversion
3. **Feature Engineering**: Date extraction, text statistics
4. **Validation**: Data quality checks and filtering

### Analysis Framework
- **Pandas**: Data manipulation and aggregation
- **NumPy**: Numerical computations
- **Matplotlib/Seaborn**: Statistical visualizations
- **Plotly**: Interactive charts
- **WordCloud**: Text visualization

### Web Application Stack
- **Streamlit**: Web framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data processing
- **Python**: Core logic

## 🔍 Usage Examples

### Basic Data Loading
```python
from src.data_loader import DataLoader

loader = DataLoader('data/metadata.csv')
df = loader.load_data()
exploration = loader.basic_exploration()
```

### Data Cleaning
```python
from src.data_cleaner import DataCleaner

cleaner = DataCleaner(df)
cleaned_df = cleaner.get_cleaned_data()
```

### Analysis
```python
from src.analyzer import DataAnalyzer

analyzer = DataAnalyzer(cleaned_df)
yearly_trends = analyzer.analyze_publications_by_year()
top_journals = analyzer.get_top_journals(20)
```

### Visualization
```python
from src.visualizer import DataVisualizer

visualizer = DataVisualizer()
fig = visualizer.plot_publications_by_year(yearly_trends)
plt.show()
```

## 📋 Requirements

### Software Requirements
- Python 3.7+
- Jupyter Notebook (optional)
- Web browser (for Streamlit app)

### Python Packages
- pandas >= 1.5.0
- matplotlib >= 3.5.0
- seaborn >= 0.11.0
- streamlit >= 1.28.0
- wordcloud >= 1.9.0
- plotly >= 5.0.0
- numpy >= 1.21.0

### System Requirements
- RAM: 4GB minimum (8GB recommended for full dataset)
- Storage: 2GB free space
- Network: Internet connection for initial setup

## 🚨 Troubleshooting

### Common Issues

**1. Memory Issues**
```python
# Use sampling for large datasets
df = loader.load_data(sample_size=10000)
```

**2. Missing WordCloud**
```bash
pip install wordcloud
```

**3. Streamlit Port Issues**
```bash
streamlit run streamlit_app.py --server.port 8502
```

**4. Data File Not Found**
- Ensure `metadata.csv` is in the `data/` directory
- Check file permissions
- Verify file is not corrupted

## 📚 Learning Outcomes

After completing this project, you will have experience with:

- **Data Science Workflow**: End-to-end data analysis pipeline
- **Python Libraries**: pandas, matplotlib, streamlit, plotly
- **Data Cleaning**: Handling real-world messy data
- **Visualization**: Creating meaningful charts and graphs
- **Web Development**: Building interactive applications
- **Version Control**: Git workflow and project organization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-analysis`)
3. Commit changes (`git commit -am 'Add new analysis feature'`)
4. Push to branch (`git push origin feature/new-analysis`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Allen Institute for AI**: For providing the CORD-19 dataset
- **Kaggle**: For hosting the dataset
- **Streamlit**: For the excellent web framework
- **Python Community**: For the amazing data science libraries

## 📞 Contact

- **Author**: Dennis Tonui
- **GitHub**: [@Kipkoech-88](https://github.com/Kipkoech-88)
- **LinkedIn**: [ Profile](https://www.linkedin.com/in/dennistonui/)

---

**Note**: This project is for educational purposes. The CORD-19 dataset is provided by the Allen Institute for AI and is subject to their terms of use.