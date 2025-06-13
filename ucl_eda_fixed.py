#!/usr/bin/env python3
"""
UEFA Champions League 2021-22 Season - Exploratory Data Analysis (Fixed Version)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os

# Configure settings
plt.style.use('default')
sns.set_palette("husl")
warnings.filterwarnings('ignore')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# Create plots directory
os.makedirs('plots', exist_ok=True)

def load_and_examine_data():
    """Load data and examine structure"""
    print("🚀 Starting UEFA Champions League 2021-22 EDA Analysis...")
    
    # Load key stats file
    try:
        key_stats = pd.read_csv('data/key_stats.csv')
        print(f"✅ Loaded key_stats: {key_stats.shape}")
        
        # Examine the problematic column
        print(f"\nExamining distance_covered column:")
        print(f"Data type: {key_stats['distance_covered'].dtype}")
        print(f"Sample values:")
        print(key_stats['distance_covered'].head(10))
        
        # Check for non-numeric values
        print(f"\nChecking for non-numeric values in distance_covered:")
        non_numeric = key_stats[pd.to_numeric(key_stats['distance_covered'], errors='coerce').isna()]
        if len(non_numeric) > 0:
            print(f"Found {len(non_numeric)} non-numeric values:")
            print(non_numeric[['player_name', 'distance_covered']].head())
        
        return key_stats
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def clean_key_stats(df):
    """Clean the key stats dataframe"""
    df_clean = df.copy()
    
    # Handle distance_covered column specifically
    print("\n🧹 Cleaning distance_covered column...")
    
    # Convert to string first to handle any mixed types
    df_clean['distance_covered'] = df_clean['distance_covered'].astype(str)
    
    # Try to extract numeric values - take only the first number if multiple are concatenated
    df_clean['distance_covered'] = df_clean['distance_covered'].str.extract('(\d+\.?\d*)')[0]
    
    # Convert to numeric
    df_clean['distance_covered'] = pd.to_numeric(df_clean['distance_covered'], errors='coerce')
    
    # Fill any remaining NaN values with 0
    df_clean['distance_covered'] = df_clean['distance_covered'].fillna(0)
    
    print(f"✅ Cleaned distance_covered. Mean: {df_clean['distance_covered'].mean():.1f}")
    
    return df_clean

def analyze_basic_stats(key_stats):
    """Generate basic statistics overview"""
    print("\n" + "="*60)
    print("KEY STATISTICS OVERVIEW")
    print("="*60)
    print(f"📈 Total players: {len(key_stats)}")
    print(f"🏟️  Total teams: {key_stats['club'].nunique()}")
    print(f"⚽ Total goals scored: {key_stats['goals'].sum()}")
    print(f"🎯 Total assists: {key_stats['assists'].sum()}")
    print(f"⏱️  Total minutes played: {key_stats['minutes_played'].sum():,}")
    print(f"🏃 Average distance per player: {key_stats['distance_covered'].mean():.1f} km")
    
    print(f"\n📊 TEAMS IN THE DATASET:")
    teams = sorted(key_stats['club'].unique())
    for i, team in enumerate(teams, 1):
        print(f"{i:2d}. {team}")
    
    return teams

def analyze_top_scorers(key_stats):
    """Analyze top scorers"""
    top_scorers = key_stats.nlargest(15, 'goals')
    
    print(f"\n🏆 TOP 15 SCORERS - UCL 2021-22")
    print("="*70)
    for idx, (_, player) in enumerate(top_scorers.iterrows(), 1):
        print(f"{idx:2d}. {player['player_name']:<25} ({player['club']:<15}) - {player['goals']} goals, {player['assists']} assists")
    
    # Get top scorer
    top_scorer = key_stats.loc[key_stats['goals'].idxmax()]
    print(f"\n🥇 GOLDEN BOOT: {top_scorer['player_name']} ({top_scorer['club']}) - {top_scorer['goals']} goals")
    
    return top_scorer, top_scorers

def create_top_scorers_plot(key_stats):
    """Create top scorers visualization"""
    plt.figure(figsize=(14, 8))
    top_10 = key_stats.nlargest(10, 'goals')
    
    bars = plt.bar(range(len(top_10)), top_10['goals'], 
                   color=plt.cm.viridis(np.linspace(0, 1, len(top_10))))
    
    plt.xlabel('Players', fontsize=12, fontweight='bold')
    plt.ylabel('Goals', fontsize=12, fontweight='bold')
    plt.title('Top 10 Goal Scorers - UEFA Champions League 2021-22', 
              fontsize=16, fontweight='bold', pad=20)
    
    # Add labels
    labels = [f"{row['player_name']}\n({row['club']})" for _, row in top_10.iterrows()]
    plt.xticks(range(len(top_10)), labels, rotation=45, ha='right')
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                 f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('plots/top_10_scorers.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✅ Saved: plots/top_10_scorers.png")

def analyze_team_performance(key_stats):
    """Analyze team performance"""
    team_stats = key_stats.groupby('club').agg({
        'goals': 'sum',
        'assists': 'sum',
        'minutes_played': 'sum',
        'match_played': 'sum',
        'distance_covered': 'sum',
        'player_name': 'count'
    }).rename(columns={'player_name': 'total_players'})
    
    team_stats = team_stats.sort_values('goals', ascending=False)
    
    print(f"\n🏆 TEAM PERFORMANCE RANKINGS")
    print("="*80)
    print(f"{'Rank':<4} {'Team':<20} {'Goals':<6} {'Assists':<7} {'Players':<8} {'Avg G/P':<8}")
    print("-"*80)
    
    for idx, (team, stats) in enumerate(team_stats.iterrows(), 1):
        avg_goals = stats['goals'] / stats['total_players'] if stats['total_players'] > 0 else 0
        print(f"{idx:<4} {team:<20} {stats['goals']:<6} {stats['assists']:<7} {stats['total_players']:<8} {avg_goals:.2f}")
    
    top_team = team_stats.index[0]
    print(f"\n🥇 HIGHEST SCORING TEAM: {top_team} with {team_stats.loc[top_team, 'goals']} goals")
    
    return team_stats, top_team

def create_team_goals_plot(team_stats):
    """Create team goals comparison plot"""
    plt.figure(figsize=(14, 10))
    
    y_pos = np.arange(len(team_stats))
    bars = plt.barh(y_pos, team_stats['goals'], 
                    color=plt.cm.tab20(np.linspace(0, 1, len(team_stats))))
    
    plt.xlabel('Total Goals', fontsize=12, fontweight='bold')
    plt.ylabel('Teams', fontsize=12, fontweight='bold')
    plt.title('Total Goals by Team - UEFA Champions League 2021-22', 
              fontsize=16, fontweight='bold', pad=20)
    
    plt.yticks(y_pos, team_stats.index)
    
    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(width + 0.5, bar.get_y() + bar.get_height()/2.,
                 f'{int(width)}', ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('plots/team_goals_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✅ Saved: plots/team_goals_comparison.png")

def load_additional_data():
    """Load other CSV files"""
    additional_data = {}
    
    files = {
        'goals': 'data/goals.csv',
        'attacking': 'data/attacking.csv'
    }
    
    for name, path in files.items():
        try:
            additional_data[name] = pd.read_csv(path)
            print(f"✅ Loaded {name}: {additional_data[name].shape}")
        except Exception as e:
            print(f"❌ Error loading {name}: {e}")
    
    return additional_data

def analyze_goals_data(goals_df):
    """Analyze goal types"""
    if 'goals' not in goals_df:
        print("❌ No goals data available")
        return
        
    print(f"\n⚽ GOAL SCORING METHODS ANALYSIS")
    print("="*60)
    
    total_goals = goals_df['goals'].sum()
    right_foot = goals_df['right_foot'].sum()
    left_foot = goals_df['left_foot'].sum()
    headers = goals_df['headers'].sum()
    penalties = goals_df['penalties'].sum()
    inside_area = goals_df['inside_area'].sum()
    outside_area = goals_df['outside_areas'].sum()
    
    print(f"Total Goals: {total_goals}")
    print(f"Right Foot: {right_foot} ({right_foot/total_goals*100:.1f}%)")
    print(f"Left Foot: {left_foot} ({left_foot/total_goals*100:.1f}%)")
    print(f"Headers: {headers} ({headers/total_goals*100:.1f}%)")
    print(f"Penalties: {penalties} ({penalties/total_goals*100:.1f}%)")
    print(f"Inside Area: {inside_area} ({inside_area/total_goals*100:.1f}%)")
    print(f"Outside Area: {outside_area} ({outside_area/total_goals*100:.1f}%)")

def create_position_analysis(key_stats):
    """Analyze performance by position"""
    position_stats = key_stats.groupby('position').agg({
        'goals': ['sum', 'mean'],
        'assists': ['sum', 'mean'],
        'player_name': 'count'
    }).round(2)
    
    position_stats.columns = ['Total Goals', 'Avg Goals', 'Total Assists', 'Avg Assists', 'Player Count']
    
    print(f"\n📊 PERFORMANCE BY POSITION")
    print("="*70)
    print(position_stats)
    
    # Create visualization
    plt.figure(figsize=(10, 6))
    position_goals = key_stats.groupby('position')['goals'].sum().sort_values(ascending=False)
    
    bars = plt.bar(position_goals.index, position_goals.values, 
                   color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
    
    plt.xlabel('Position', fontsize=12, fontweight='bold')
    plt.ylabel('Total Goals', fontsize=12, fontweight='bold')
    plt.title('Total Goals by Position - UCL 2021-22', fontsize=14, fontweight='bold', pad=20)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                 f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('plots/goals_by_position.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✅ Saved: plots/goals_by_position.png")

def generate_final_summary(key_stats, top_scorer, top_team, team_stats):
    """Generate final summary"""
    print("\n" + "="*60)
    print("🏆 FINAL TOURNAMENT SUMMARY")
    print("="*60)
    
    total_players = len(key_stats)
    total_teams = key_stats['club'].nunique()
    total_goals = key_stats['goals'].sum()
    total_assists = key_stats['assists'].sum()
    
    # Top assister
    top_assister = key_stats.loc[key_stats['assists'].idxmax()]
    
    print(f"📈 Total Players Analyzed: {total_players}")
    print(f"🏟️  Teams Participating: {total_teams}")
    print(f"⚽ Total Goals Scored: {total_goals}")
    print(f"🎯 Total Assists: {total_assists}")
    print(f"📊 Average Goals per Team: {total_goals/total_teams:.1f}")
    
    print(f"\n🥇 Golden Boot Winner: {top_scorer['player_name']} ({top_scorer['goals']} goals)")
    print(f"🎖️  Top Assist Provider: {top_assister['player_name']} ({top_assister['assists']} assists)")
    print(f"🏆 Highest Scoring Team: {top_team} ({team_stats.loc[top_team, 'goals']} goals)")
    
    print("\n" + "="*60)
    print("✅ EDA ANALYSIS COMPLETE!")
    print("📁 All visualizations saved to 'plots/' directory")

def main():
    """Main function"""
    # Load and examine data
    key_stats = load_and_examine_data()
    if key_stats is None:
        return
    
    # Clean the data
    key_stats_clean = clean_key_stats(key_stats)
    
    # Basic analysis
    teams = analyze_basic_stats(key_stats_clean)
    
    # Top scorers
    top_scorer, top_scorers = analyze_top_scorers(key_stats_clean)
    create_top_scorers_plot(key_stats_clean)
    
    # Team performance
    team_stats, top_team = analyze_team_performance(key_stats_clean)
    create_team_goals_plot(team_stats)
    
    # Position analysis
    create_position_analysis(key_stats_clean)
    
    # Load additional data
    additional_data = load_additional_data()
    
    # Analyze goals if available
    if 'goals' in additional_data:
        analyze_goals_data(additional_data['goals'])
    
    # Final summary
    generate_final_summary(key_stats_clean, top_scorer, top_team, team_stats)

if __name__ == "__main__":
    main() 