# UEFA Champions League 2021-22 Data Analysis Project

A comprehensive data analysis and interactive dashboard project for the UEFA Champions League 2021-22 season.

## 🏆 Project Overview

This project provides in-depth analysis of the UEFA Champions League 2021-22 season, featuring:
- **Exploratory Data Analysis (EDA)** with statistical insights
- **Interactive Streamlit Dashboard** with multiple pages
- **Data visualizations** using Matplotlib, Seaborn, and Plotly
- **Player and team performance analysis**

## 📊 Key Features

### EDA Analysis
- ⚽ **Goal Scoring Analysis**: Top scorers, goal types, scoring methods
- 🏟️ **Team Performance**: Team rankings, goals, assists, efficiency metrics
- 👤 **Player Statistics**: Individual performance metrics and comparisons
- 📈 **Position Analysis**: Performance breakdown by player positions
- 🎯 **Advanced Metrics**: Goals per 90 minutes, goal contributions, efficiency

### Interactive Dashboard
- **🏠 Overview**: Tournament summary and key metrics
- **👤 Top Players**: Filterable player analysis and search
- **🏟️ Team Analysis**: Team comparison and rankings
- **⚽ Goals & Scoring**: Detailed goal analysis and penalty statistics
- **📊 Statistical Insights**: Correlations and advanced metrics
- **🔍 Match Explorer**: Head-to-head team comparisons

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone/Download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the dataset** (run once):
   ```python
   python3 -c "import kagglehub; path = kagglehub.dataset_download('azminetoushikwasi/ucl-202122-uefa-champions-league'); print('Path to dataset files:', path)"
   ```

4. **Run the EDA analysis**:
   ```bash
   python3 ucl_eda_fixed.py
   ```

5. **Launch the interactive dashboard**:
   ```bash
   streamlit run ucl_dashboard.py
   ```

## 📁 Project Structure

```
UCL_Data_Analyst/
├── data/                    # Dataset CSV files
│   ├── key_stats.csv       # Main player statistics
│   ├── goals.csv           # Goal scoring details
│   ├── attacking.csv       # Attacking statistics
│   ├── defending.csv       # Defensive statistics
│   ├── goalkeeping.csv     # Goalkeeper statistics
│   ├── disciplinary.csv    # Cards and disciplinary actions
│   ├── attempts.csv        # Shot attempts data
│   └── distributon.csv     # Pass distribution data
├── plots/                   # Generated visualizations
│   ├── top_10_scorers.png
│   ├── team_goals_comparison.png
│   ├── goals_by_position.png
│   └── goal_analysis_detailed.png
├── notebooks/               # Jupyter notebooks
│   └── ucl_eda_analysis.ipynb
├── ucl_eda_fixed.py        # Main EDA analysis script
├── ucl_dashboard.py        # Streamlit dashboard
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## 📈 Key Insights Discovered

### Tournament Highlights
- **🥇 Golden Boot Winner**: Benzema (Real Madrid) with 15 goals
- **🎖️ Top Assist Provider**: Bruno Fernandes (Man. United) with 7 assists
- **🏆 Highest Scoring Team**: Bayern Munich with 30 goals
- **📊 Total Goals**: 368 goals across all teams
- **🏟️ Teams Analyzed**: 32 teams with 747 players

### Scoring Patterns
- **Right Foot Goals**: 48.1% of all goals
- **Left Foot Goals**: 34.3% of all goals
- **Headers**: 16.2% of all goals
- **Inside Area**: 89.7% of goals scored inside the penalty area
- **Penalties**: 9.7% of goals from penalties

### Team Performance
- **Top 5 Teams by Goals**: Bayern (30), Real Madrid (28), Man. City (28), Liverpool (28), Ajax (21)
- **Most Efficient Teams**: Bayern (1.25 goals per player), Real Madrid (1.12), Man. City (1.08)

## 🛠️ Technologies Used

- **Python 3.10+**
- **Data Analysis**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Dashboard**: Streamlit
- **Data Source**: Kaggle (via kagglehub)

## 📊 Dashboard Features

### Interactive Elements
- **Filters**: Team selection, position filtering, minimum minutes played
- **Search**: Individual player lookup
- **Comparisons**: Side-by-side team analysis
- **Drill-down**: Detailed statistics for players and teams

### Visualization Types
- Bar charts for rankings and comparisons
- Scatter plots for correlations
- Pie charts for distributions
- Heatmaps for correlations
- Interactive tables with sorting

## 🎯 Use Cases

1. **Scout Analysis**: Identify top performers and emerging talents
2. **Team Strategy**: Analyze opponent strengths and weaknesses
3. **Performance Tracking**: Monitor player and team metrics
4. **Historical Analysis**: Compare current season with historical data
5. **Media & Reporting**: Generate insights for sports journalism

## 🔄 Running the Analysis

### Step-by-Step Execution

1. **Data Download & Setup**:
   ```bash
   # Download dataset
   python3 -c "import kagglehub; kagglehub.dataset_download('azminetoushikwasi/ucl-202122-uefa-champions-league')"
   ```

2. **EDA Analysis**:
   ```bash
   # Generate all visualizations and insights
   python3 ucl_eda_fixed.py
   ```

3. **Interactive Dashboard**:
   ```bash
   # Launch web dashboard
   streamlit run ucl_dashboard.py
   ```

4. **Jupyter Notebook** (Optional):
   ```bash
   # For detailed exploration
   jupyter notebook notebooks/ucl_eda_analysis.ipynb
   ```

## 📋 Output Files

### Generated Visualizations
- `plots/top_10_scorers.png` - Top goal scorers chart
- `plots/team_goals_comparison.png` - Team performance comparison
- `plots/goals_by_position.png` - Position-wise goal distribution
- `plots/goal_analysis_detailed.png` - Detailed goal type analysis

### Dashboard Access
- Local URL: `http://localhost:8501` (after running Streamlit)
- Multi-page interface with navigation sidebar
- Responsive design for desktop and mobile

## 🤝 Contributing

Feel free to contribute to this project by:
- Adding new analysis features
- Improving visualizations
- Enhancing the dashboard UI
- Adding more detailed insights

## 📄 License

This project is for educational and analysis purposes. Dataset sourced from Kaggle under their respective licensing terms.

## 🔗 Data Source

- **Dataset**: UEFA Champions League 2021-22
- **Source**: [Kaggle](https://www.kaggle.com/datasets/azminetoushikwasi/ucl-202122-uefa-champions-league)
- **Author**: Azmine Toushik Wasi

---

*Built with ❤️ for football analytics enthusiasts* 