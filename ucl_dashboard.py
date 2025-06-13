#!/usr/bin/env python3
"""
UEFA Champions League 2021-22 Interactive Dashboard
Multi-page Streamlit application for exploring UCL data
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import warnings

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="UEFA Champions League 2021-22 Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cache data loading
@st.cache_data
def load_data():
    """Load and clean all datasets"""
    try:
        # Load datasets
        key_stats = pd.read_csv('data/key_stats.csv')
        goals = pd.read_csv('data/goals.csv')
        attacking = pd.read_csv('data/attacking.csv')
        defending = pd.read_csv('data/defending.csv')
        goalkeeping = pd.read_csv('data/goalkeeping.csv')
        
        # Clean key stats distance_covered column
        key_stats['distance_covered'] = key_stats['distance_covered'].astype(str)
        key_stats['distance_covered'] = key_stats['distance_covered'].str.extract('(\d+\.?\d*)')[0]
        key_stats['distance_covered'] = pd.to_numeric(key_stats['distance_covered'], errors='coerce').fillna(0)
        
        return {
            'key_stats': key_stats,
            'goals': goals,
            'attacking': attacking,
            'defending': defending,
            'goalkeeping': goalkeeping
        }
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load data
data = load_data()

if data is None:
    st.error("Failed to load data. Please check if the data files exist.")
    st.stop()

# Sidebar navigation
st.sidebar.title("🏆 UCL 2021-22 Dashboard")
st.sidebar.markdown("---")

pages = {
    "🏠 Overview": "overview",
    "👤 Top Players": "players", 
    "🏟️ Team Analysis": "teams",
    "⚽ Goals & Scoring": "goals",
    "📊 Statistical Insights": "stats",
    "🔍 Match Explorer": "matches"
}

selected_page = st.sidebar.selectbox("Select Page", list(pages.keys()))
page = pages[selected_page]

# Main title
st.title("⚽ UEFA Champions League 2021-22 Analysis Dashboard")
st.markdown("---")

# Page content
if page == "overview":
    st.header("🏠 Tournament Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Players", len(data['key_stats']))
    with col2:
        st.metric("Teams", data['key_stats']['club'].nunique())
    with col3:
        st.metric("Total Goals", data['key_stats']['goals'].sum())
    with col4:
        st.metric("Total Assists", data['key_stats']['assists'].sum())
    
    st.markdown("---")
    
    # Overview charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Goals by Position")
        position_goals = data['key_stats'].groupby('position')['goals'].sum().reset_index()
        fig = px.bar(position_goals, x='position', y='goals', 
                     color='goals', color_continuous_scale='viridis',
                     title="Total Goals by Position")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🏆 Top 10 Teams by Goals")
        team_goals = data['key_stats'].groupby('club')['goals'].sum().sort_values(ascending=False).head(10)
        fig = px.bar(x=team_goals.values, y=team_goals.index, 
                     orientation='h', color=team_goals.values,
                     color_continuous_scale='plasma',
                     title="Goals Scored by Team")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Tournament insights
    st.subheader("🔍 Key Tournament Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        top_scorer = data['key_stats'].loc[data['key_stats']['goals'].idxmax()]
        st.metric("🥇 Golden Boot Winner", 
                 f"{top_scorer['player_name']}", 
                 f"{top_scorer['goals']} goals")
    
    with col2:
        top_assister = data['key_stats'].loc[data['key_stats']['assists'].idxmax()]
        st.metric("🎯 Top Assist Provider", 
                 f"{top_assister['player_name']}", 
                 f"{top_assister['assists']} assists")
    
    with col3:
        top_team = data['key_stats'].groupby('club')['goals'].sum().idxmax()
        team_goals_count = data['key_stats'].groupby('club')['goals'].sum().max()
        st.metric("🏆 Highest Scoring Team", 
                 f"{top_team}", 
                 f"{team_goals_count} goals")

elif page == "players":
    st.header("👤 Top Players Analysis")
    
    # Player filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_teams = st.multiselect("Select Teams", 
                                       options=sorted(data['key_stats']['club'].unique()),
                                       default=None)
    with col2:
        selected_positions = st.multiselect("Select Positions", 
                                           options=data['key_stats']['position'].unique(),
                                           default=None)
    with col3:
        min_minutes = st.slider("Minimum Minutes Played", 0, 1500, 0)
    
    # Filter data
    filtered_data = data['key_stats'].copy()
    if selected_teams:
        filtered_data = filtered_data[filtered_data['club'].isin(selected_teams)]
    if selected_positions:
        filtered_data = filtered_data[filtered_data['position'].isin(selected_positions)]
    filtered_data = filtered_data[filtered_data['minutes_played'] >= min_minutes]
    
    # Top scorers
    st.subheader("🥅 Top Goal Scorers")
    top_scorers = filtered_data.nlargest(15, 'goals')[['player_name', 'club', 'position', 'goals', 'assists', 'match_played']]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.bar(top_scorers, x='player_name', y='goals', 
                     color='club', hover_data=['assists', 'match_played'],
                     title="Top 15 Goal Scorers")
        fig.update_xaxes(tickangle=45)
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.dataframe(top_scorers, height=500)
    
    # Goals vs Assists scatter
    st.subheader("⚽ Goals vs Assists Analysis")
    
    active_players = filtered_data[(filtered_data['goals'] > 0) | (filtered_data['assists'] > 0)]
    
    fig = px.scatter(active_players, x='goals', y='assists', 
                     size='match_played', color='position',
                     hover_data=['player_name', 'club', 'minutes_played'],
                     title="Goals vs Assists (Bubble size = Matches Played)")
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Player search
    st.subheader("🔍 Player Search")
    player_name = st.selectbox("Search for a specific player:", 
                              options=[''] + sorted(data['key_stats']['player_name'].unique()))
    
    if player_name:
        player_data = data['key_stats'][data['key_stats']['player_name'] == player_name].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Goals", player_data['goals'])
            st.metric("Assists", player_data['assists'])
        with col2:
            st.metric("Minutes Played", f"{player_data['minutes_played']:,}")
            st.metric("Matches Played", player_data['match_played'])
        with col3:
            st.metric("Club", player_data['club'])
            st.metric("Position", player_data['position'])

elif page == "teams":
    st.header("🏟️ Team Analysis")
    
    # Team comparison
    team_stats = data['key_stats'].groupby('club').agg({
        'goals': 'sum',
        'assists': 'sum', 
        'minutes_played': 'sum',
        'distance_covered': 'sum',
        'player_name': 'count'
    }).rename(columns={'player_name': 'total_players'}).round(2)
    
    team_stats['goals_per_player'] = (team_stats['goals'] / team_stats['total_players']).round(2)
    team_stats = team_stats.sort_values('goals', ascending=False)
    
    # Team selector
    selected_teams_compare = st.multiselect("Select teams to compare:", 
                                           options=team_stats.index.tolist(),
                                           default=team_stats.index[:5].tolist())
    
    if selected_teams_compare:
        # Team comparison chart
        comparison_data = team_stats.loc[selected_teams_compare]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Goals Comparison")
            fig = px.bar(comparison_data.reset_index(), x='club', y='goals',
                        color='goals', color_continuous_scale='blues',
                        title="Total Goals by Team")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Assists Comparison")
            fig = px.bar(comparison_data.reset_index(), x='club', y='assists',
                        color='assists', color_continuous_scale='greens',
                        title="Total Assists by Team")
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed team stats table
        st.subheader("📈 Detailed Team Statistics")
        st.dataframe(comparison_data, use_container_width=True)
    
    # Overall team rankings
    st.subheader("🏆 Complete Team Rankings")
    
    # Add ranking column
    team_stats_display = team_stats.reset_index()
    team_stats_display['rank'] = range(1, len(team_stats_display) + 1)
    
    st.dataframe(team_stats_display[['rank', 'club', 'goals', 'assists', 'total_players', 'goals_per_player']], 
                use_container_width=True)

elif page == "goals":
    st.header("⚽ Goals & Scoring Analysis")
    
    if 'goals' in data:
        goals_df = data['goals']
        
        # Goal type analysis
        st.subheader("🎯 Goal Scoring Methods")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart for foot preference
            foot_data = {
                'Right Foot': goals_df['right_foot'].sum(),
                'Left Foot': goals_df['left_foot'].sum(), 
                'Headers': goals_df['headers'].sum()
            }
            
            fig = px.pie(values=list(foot_data.values()), names=list(foot_data.keys()),
                        title="Goals by Scoring Method")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Pie chart for area
            area_data = {
                'Inside Area': goals_df['inside_area'].sum(),
                'Outside Area': goals_df['outside_areas'].sum()
            }
            
            fig = px.pie(values=list(area_data.values()), names=list(area_data.keys()),
                        title="Goals by Area")
            st.plotly_chart(fig, use_container_width=True)
        
        # Goal statistics
        col1, col2, col3, col4 = st.columns(4)
        
        total_goals = goals_df['goals'].sum()
        with col1:
            st.metric("Total Goals", total_goals)
        with col2:
            st.metric("Penalties", goals_df['penalties'].sum())
        with col3:
            st.metric("Headers", goals_df['headers'].sum())
        with col4:
            st.metric("Outside Area", goals_df['outside_areas'].sum())
        
        # Top penalty takers
        st.subheader("🥅 Penalty Specialists")
        penalty_takers = goals_df[goals_df['penalties'] > 0].nlargest(10, 'penalties')[['player_name', 'club', 'penalties', 'goals']]
        
        if not penalty_takers.empty:
            fig = px.bar(penalty_takers, x='player_name', y='penalties',
                        color='club', hover_data=['goals'],
                        title="Top Penalty Scorers")
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        # Goals per match efficiency
        st.subheader("📈 Scoring Efficiency")
        goals_df['goals_per_match'] = goals_df['goals'] / goals_df['match_played']
        efficiency = goals_df[goals_df['goals'] >= 3].nlargest(15, 'goals_per_match')[['player_name', 'club', 'goals', 'match_played', 'goals_per_match']]
        
        fig = px.bar(efficiency, x='player_name', y='goals_per_match',
                    color='goals_per_match', color_continuous_scale='reds',
                    hover_data=['goals', 'match_played'],
                    title="Goals per Match Ratio (Min 3 goals)")
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

elif page == "stats":
    st.header("📊 Statistical Insights")
    
    # Performance by position
    st.subheader("📈 Performance by Position")
    
    position_stats = data['key_stats'].groupby('position').agg({
        'goals': ['sum', 'mean'],
        'assists': ['sum', 'mean'],
        'minutes_played': ['sum', 'mean'],
        'player_name': 'count'
    }).round(2)
    
    position_stats.columns = ['Total Goals', 'Avg Goals', 'Total Assists', 'Avg Assists', 
                              'Total Minutes', 'Avg Minutes', 'Player Count']
    
    st.dataframe(position_stats, use_container_width=True)
    
    # Correlation analysis
    st.subheader("🔗 Performance Correlations")
    
    numeric_cols = ['goals', 'assists', 'minutes_played', 'match_played', 'distance_covered']
    correlation_data = data['key_stats'][numeric_cols].corr()
    
    fig = px.imshow(correlation_data, 
                    text_auto=True, aspect="auto",
                    title="Correlation Matrix of Player Performance Metrics")
    st.plotly_chart(fig, use_container_width=True)
    
    # Distribution analysis
    st.subheader("📊 Performance Distributions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.histogram(data['key_stats'], x='goals', nbins=20,
                          title="Distribution of Goals Scored")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.histogram(data['key_stats'], x='assists', nbins=20,
                          title="Distribution of Assists")
        st.plotly_chart(fig, use_container_width=True)
    
    # Advanced metrics
    st.subheader("🎯 Advanced Player Metrics")
    
    # Calculate advanced stats
    data['key_stats']['goal_contribution'] = data['key_stats']['goals'] + data['key_stats']['assists']
    data['key_stats']['minutes_per_goal'] = data['key_stats']['minutes_played'] / (data['key_stats']['goals'] + 0.1)
    data['key_stats']['goals_per_90'] = (data['key_stats']['goals'] / data['key_stats']['minutes_played']) * 90
    
    advanced_stats = data['key_stats'][data['key_stats']['minutes_played'] >= 300].nlargest(15, 'goal_contribution')[
        ['player_name', 'club', 'goal_contribution', 'goals_per_90', 'minutes_per_goal']
    ].round(2)
    
    st.dataframe(advanced_stats, use_container_width=True)

elif page == "matches":
    st.header("🔍 Match Explorer")
    
    st.subheader("🏟️ Team vs Team Analysis")
    
    # Team selector for comparison
    col1, col2 = st.columns(2)
    
    with col1:
        team1 = st.selectbox("Select Team 1:", options=sorted(data['key_stats']['club'].unique()))
    
    with col2:
        team2 = st.selectbox("Select Team 2:", options=sorted(data['key_stats']['club'].unique()))
    
    if team1 and team2 and team1 != team2:
        # Compare teams
        team1_data = data['key_stats'][data['key_stats']['club'] == team1]
        team2_data = data['key_stats'][data['key_stats']['club'] == team2]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(f"{team1} Goals", team1_data['goals'].sum())
            st.metric(f"{team2} Goals", team2_data['goals'].sum())
        
        with col2:
            st.metric(f"{team1} Assists", team1_data['assists'].sum())
            st.metric(f"{team2} Assists", team2_data['assists'].sum())
        
        with col3:
            st.metric(f"{team1} Players", len(team1_data))
            st.metric(f"{team2} Players", len(team2_data))
        
        # Head to head visualization
        comparison_df = pd.DataFrame({
            'Team': [team1, team2],
            'Goals': [team1_data['goals'].sum(), team2_data['goals'].sum()],
            'Assists': [team1_data['assists'].sum(), team2_data['assists'].sum()],
            'Total Minutes': [team1_data['minutes_played'].sum(), team2_data['minutes_played'].sum()]
        })
        
        fig = px.bar(comparison_df, x='Team', y=['Goals', 'Assists'], 
                    title=f"{team1} vs {team2} - Goals and Assists Comparison",
                    barmode='group')
        st.plotly_chart(fig, use_container_width=True)
        
        # Player comparison
        st.subheader("👥 Top Players Comparison")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**{team1} Top Scorers:**")
            team1_top = team1_data.nlargest(5, 'goals')[['player_name', 'goals', 'assists']]
            st.dataframe(team1_top, hide_index=True)
        
        with col2:
            st.write(f"**{team2} Top Scorers:**")
            team2_top = team2_data.nlargest(5, 'goals')[['player_name', 'goals', 'assists']]
            st.dataframe(team2_top, hide_index=True)

# Footer
st.markdown("---")
st.markdown("*Dashboard created for UEFA Champions League 2021-22 season analysis*")
st.markdown("*Data source: Kaggle UCL 2021-22 Dataset*") 