# UEFA Champions League 2021-22 Data Analysis Dashboard

## 🚀 Live Demo
**🌐 Deployed Application**: [https://ucl-data-analyst.vercel.app](https://ucl-data-analyst.vercel.app)

**📊 Featured Pages**:
- [Team Analysis](https://ucl-data-analyst.vercel.app/teams) - Interactive team comparison and statistics
- [Player Analysis](https://ucl-data-analyst.vercel.app/players) - Advanced player filtering and analytics
- [Goals & Scoring](https://ucl-data-analyst.vercel.app/goals) - Goal analysis and scoring patterns
- [Match Explorer](https://ucl-data-analyst.vercel.app/matches) - Match analysis and insights

## Overview
This project provides a comprehensive analysis of the UEFA Champions League 2021-22 season through interactive dashboards and data visualizations. The analysis covers player statistics, team performance, match insights, and tactical analysis.

**🏆 Key Highlights from Live Data**:
- **Champion**: Man. United (30 points)
- **Top Scorer**: Bayern (30 goals)
- **Best Defense**: Salzburg (5 goals conceded)
- **Possession Leaders**: Inter (64.8%)

## Features

### 🏠 Dashboard Overview
- Interactive Streamlit dashboard with multiple analysis pages
- Real-time data filtering and visualization
- Comprehensive tournament statistics

### 👤 Player Analysis
- Individual player performance metrics
- Goals, assists, and playing time analysis
- Position-based comparisons
- Player search and filtering capabilities

### 🏟️ Team Analysis
- Team performance comparisons
- Goals scored vs conceded analysis
- Team rankings and statistics
- Interactive team comparison tools

### ⚽ Goals & Scoring Analysis
- Goal distribution analysis
- Scoring patterns and trends
- Top scorers identification
- Match-by-match goal analysis

### 📊 Statistical Insights
- Advanced statistical analysis
- Performance correlations
- Predictive insights
- Data-driven recommendations

### 🔍 Match Explorer
- Individual match analysis
- Head-to-head comparisons
- Match outcome predictions
- Historical match data

## Technical Stack

### Backend
- **Python 3.9+**: Core programming language
- **Django**: Web framework for backend API
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Streamlit**: Interactive dashboard framework

### Frontend
- **HTML5/CSS3**: Modern web standards
- **Bootstrap 5**: Responsive UI framework
- **JavaScript**: Interactive functionality
- **Chart.js**: Data visualization library

### Data Visualization
- **Plotly**: Interactive charts and graphs
- **Matplotlib**: Statistical plotting
- **Seaborn**: Statistical data visualization

### Deployment
- **Vercel**: Cloud deployment platform
- **Git**: Version control
- **GitHub**: Code repository

## Data Sources
The analysis is based on official UEFA Champions League 2021-22 data including:
- Player statistics (goals, assists, minutes played, etc.)
- Team performance data
- Match results and fixtures
- Advanced metrics (xG, possession, etc.)

## Installation & Setup

### Prerequisites
- Python 3.9 or higher
- Node.js (for Vercel CLI)
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/aneesh1308/UCL-Data-Analyst.git
   cd UCL-Data-Analyst
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Django migrations**
   ```bash
   python manage.py migrate
   ```

5. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Run Streamlit dashboard** (in separate terminal)
   ```bash
   streamlit run ucl_dashboard.py
   ```

### Deployment

The application is configured for deployment on Vercel with the following setup:

1. **Vercel Configuration** (`vercel.json`)
   - Python 3.9 runtime
   - Django WSGI application
   - Static file serving
   - Environment variables

2. **Build Script** (`build_files.sh`)
   - Automated dependency installation
   - Database migrations
   - Static file collection

3. **Deployment Process**
   ```bash
   git add .
   git commit -m "Your commit message"
   git push origin master
   ```

## 🌐 Live Deployment

**Production URL**: [https://ucl-data-analyst.vercel.app](https://ucl-data-analyst.vercel.app)

### Deployment Status
- ✅ **Deployed on Vercel**: Serverless deployment with automatic scaling
- ✅ **Public Access**: No authentication required - open to all users
- ✅ **AJAX Functionality**: Real-time filtering and comparison without page reloads
- ✅ **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- ✅ **Performance Optimized**: Fast loading with efficient data processing
- ✅ **SEO Friendly**: Proper meta tags and structured data

### Live Features Working
- **Team Comparison**: Interactive AJAX-powered team comparison tool
- **Player Filtering**: Real-time player filtering by position, team, and performance
- **Data Visualization**: Interactive charts using Chart.js
- **Pagination**: Smooth pagination without page reloads
- **Dark Theme**: Modern UI with proper contrast and accessibility

## Project Structure

```
UCL-Data-Analyst/
├── data/                          # Raw data files
│   ├── key_stats.csv
│   ├── goals.csv
│   ├── attacking.csv
│   ├── defending.csv
│   └── goalkeeping.csv
├── templates/                     # HTML templates
│   └── dashboard/
│       ├── base.html
│       ├── players_enhanced.html
│       ├── teams.html
│       └── ...
├── staticfiles/                   # Static assets
├── ucl_analytics/                 # Django application
├── notebooks/                     # Jupyter notebooks
├── plots/                         # Generated visualizations
├── ucl_dashboard.py              # Streamlit dashboard
├── ucl_eda_analysis.py           # Data analysis scripts
├── manage.py                     # Django management
├── requirements.txt              # Python dependencies
├── vercel.json                   # Vercel configuration
├── build_files.sh               # Build script
└── README.md                    # Project documentation
```

## Key Features Implementation

### Player Analysis Dashboard
- **Enhanced Filtering**: Position, team, and performance-based filters
- **Interactive Visualizations**: Goals vs assists scatter plots, performance metrics
- **Player Comparison**: Side-by-side player statistics
- **Search Functionality**: Quick player lookup and detailed stats

### Team Comparison System
- **Head-to-Head Analysis**: Direct team comparisons
- **Performance Metrics**: Goals, assists, win rates, player counts
- **Visual Comparisons**: Interactive charts and graphs
- **Pagination**: Organized team listings with navigation

### Advanced Analytics
- **Performance Ratings**: Custom player performance calculations
- **Market Value Estimates**: Player valuation based on performance
- **Fitness Scores**: Player fitness and availability metrics
- **Tactical Analysis**: Formation and strategy insights

## Data Analysis Insights

### Key Tournament Statistics
- **Total Players Analyzed**: 500+ players
- **Teams Covered**: 32 teams
- **Matches Analyzed**: 125+ matches
- **Goals Tracked**: 400+ goals
- **Assists Recorded**: 300+ assists

### Top Performers Identification
- **Golden Boot Winner**: Highest goal scorer
- **Best Playmaker**: Most assists provided
- **Most Valuable Player**: Performance-based ranking
- **Best Team**: Overall tournament performance

### Performance Categories
- **Elite Performers**: Top 10% of players
- **Consistent Players**: Regular contributors
- **Emerging Talents**: Young player highlights
- **Team Leaders**: Captain and key player analysis

## Technical Improvements

### UI/UX Enhancements
- **Dark Theme**: Modern dark mode interface
- **Responsive Design**: Mobile and tablet compatibility
- **Color Accessibility**: High contrast for better visibility
- **Interactive Elements**: Hover effects and smooth transitions

### Performance Optimizations
- **Data Caching**: Efficient data loading and storage
- **Lazy Loading**: On-demand content loading
- **Optimized Queries**: Efficient database operations
- **Static File Optimization**: Compressed assets

### Security Features
- **Input Validation**: Secure form handling
- **CSRF Protection**: Cross-site request forgery prevention
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Cross-site scripting mitigation

## Future Enhancements

### Planned Features
- **Real-time Data Updates**: Live match data integration
- **Machine Learning Predictions**: Player performance forecasting
- **Advanced Visualizations**: 3D charts and interactive maps
- **Mobile Application**: Native mobile app development

### Data Expansion
- **Historical Data**: Multi-season analysis
- **Player Transfer Data**: Market movement tracking
- **Injury Reports**: Player availability tracking
- **Social Media Sentiment**: Fan engagement analysis

## Contributing

We welcome contributions to improve the UEFA Champions League analysis dashboard. Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests if applicable**
5. **Submit a pull request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to functions
- Include unit tests for new features
- Update documentation as needed

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For questions, suggestions, or collaboration opportunities:

- **GitHub**: [aneesh1308](https://github.com/aneesh1308)
- **Project Repository**: [UCL-Data-Analyst](https://github.com/aneesh1308/UCL-Data-Analyst)

## Acknowledgments

- UEFA for providing official tournament data
- The open-source community for excellent libraries and tools
- Contributors and collaborators who helped improve this project

---

**Last Updated**: December 2024 - Deployment Trigger
**Version**: 2.1.0
**Status**: Active Development 