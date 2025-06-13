#!/usr/bin/env python3
"""
UEFA Champions League 2021-22 Season - Exploratory Data Analysis
Comprehensive analysis of player and team performance data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os
from datetime import datetime

# Configure settings
plt.style.use('default')
sns.set_palette("husl")
warnings.filterwarnings('ignore')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# Create plots directory
os.makedirs('plots', exist_ok=True)

def load_data():
    """Load all CSV files"""
    data_files = {
        'key_stats': 'data/key_stats.csv',
        'goals': 'data/goals.csv',
        'attacking': 'data/attacking.csv',
        'defending': 'data/defending.csv',
        'goalkeeping': 'data/goalkeeping.csv',
        'disciplinary': 'data/disciplinary.csv',
        'attempts': 'data/attempts.csv',
        'distribution': 'data/distributon.csv'  # Note: typo in original filename
    }
    
    dfs = {}
    for name, path in data_files.items():
        try:
            dfs[name] = pd.read_csv(path)
            print(f"✅ Loaded {name}: {dfs[name].shape[0]} rows, {dfs[name].shape[1]} columns")
        except FileNotFoundError:
            print(f"❌ File not found: {path}")
        except Exception as e:
            print(f"❌ Error loading {name}: {str(e)}")
    
    return dfs

def clean_data(dfs):
    """Clean and standardize all dataframes"""
    clean_dfs = {}
    
    for name, df in dfs.items():
        df_clean = df.copy()
        
        # Standardize names
        if 'player_name' in df_clean.columns:
            df_clean['player_name'] = df_clean['player_name'].str.strip()
        if 'club' in df_clean.columns:
            df_clean['club'] = df_clean['club'].str.strip()
        
        # Convert numeric columns
        numeric_columns = df_clean.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        
        # Fill missing values
        df_clean = df_clean.fillna(0)
        
        clean_dfs[name] = df_clean
        print(f"✅ Cleaned {name}: {df_clean.shape}")
    
    return clean_dfs

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
        print(f"{idx:2d}. {player['player_name']:<20} ({player['club']:<15}) - {player['goals']} goals, {player['assists']} assists")
    
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

def create_goals_assists_plot(key_stats):
    """Create goals vs assists scatter plot"""
    plt.figure(figsize=(12, 8))
    
    # Filter active players
    active_players = key_stats[(key_stats['goals'] > 0) | (key_stats['assists'] > 0)]
    
    scatter = plt.scatter(active_players['goals'], active_players['assists'], 
                         s=active_players['match_played']*10, alpha=0.6, 
                         c=active_players['minutes_played'], cmap='viridis')
    
    plt.xlabel('Goals', fontsize=12, fontweight='bold')
    plt.ylabel('Assists', fontsize=12, fontweight='bold')
    plt.title('Goals vs Assists (Bubble size = Matches, Color = Minutes)', 
              fontsize=14, fontweight='bold', pad=20)
    
    # Add colorbar
    cbar = plt.colorbar(scatter)
    cbar.set_label('Minutes Played', fontsize=10)
    
    # Annotate top performers
    top_performers = active_players.nlargest(5, 'goals')
    for _, player in top_performers.iterrows():
        plt.annotate(player['player_name'], 
                    (player['goals'], player['assists']),
                    xytext=(5, 5), textcoords='offset points', fontsize=9)
    
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('plots/goals_vs_assists.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✅ Saved: plots/goals_vs_assists.png")

def analyze_positions(key_stats):
    """Analyze performance by position"""
    position_stats = key_stats.groupby('position').agg({
        'goals': ['sum', 'mean'],
        'assists': ['sum', 'mean'],
        'minutes_played': ['sum', 'mean'],
        'player_name': 'count'
    }).round(2)
    
    position_stats.columns = ['Total Goals', 'Avg Goals', 'Total Assists', 'Avg Assists', 
                              'Total Minutes', 'Avg Minutes', 'Player Count']
    
    print(f"\n📊 PERFORMANCE BY POSITION")
    print("="*90)
    print(position_stats)
    
    return position_stats

def create_position_plot(key_stats):
    """Create goals by position plot"""
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

def analyze_goal_types(goals_df):
    """Analyze goal types from goals dataset"""
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
    
    return {
        'total': total_goals, 'right_foot': right_foot, 'left_foot': left_foot,
        'headers': headers, 'penalties': penalties, 'inside_area': inside_area,
        'outside_area': outside_area
    }

def create_goal_analysis_plot(goals_df, goal_stats):
    """Create detailed goal analysis plots"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Pie chart 1: Scoring method
    method_data = [goal_stats['right_foot'], goal_stats['left_foot'], goal_stats['headers']]
    method_labels = ['Right Foot', 'Left Foot', 'Headers']
    ax1.pie(method_data, labels=method_labels, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Goals by Scoring Method', fontweight='bold')
    
    # Pie chart 2: Area analysis
    area_data = [goal_stats['inside_area'], goal_stats['outside_area']]
    area_labels = ['Inside Area', 'Outside Area']
    ax2.pie(area_data, labels=area_labels, autopct='%1.1f%%', startangle=90)
    ax2.set_title('Goals by Area', fontweight='bold')
    
    # Bar chart: Top penalty takers
    penalty_takers = goals_df[goals_df['penalties'] > 0].nlargest(8, 'penalties')
    ax3.bar(range(len(penalty_takers)), penalty_takers['penalties'])
    ax3.set_xlabel('Players')
    ax3.set_ylabel('Penalties Scored')
    ax3.set_title('Top Penalty Scorers', fontweight='bold')
    ax3.set_xticks(range(len(penalty_takers)))
    ax3.set_xticklabels([name[:10] for name in penalty_takers['player_name']], rotation=45)
    
    # Bar chart: Goals per match
    goals_df['goals_per_match'] = goals_df['goals'] / goals_df['match_played']
    top_ratio = goals_df.nlargest(10, 'goals_per_match')
    ax4.bar(range(len(top_ratio)), top_ratio['goals_per_match'])
    ax4.set_xlabel('Players')
    ax4.set_ylabel('Goals per Match')
    ax4.set_title('Highest Goals per Match Ratio', fontweight='bold')
    ax4.set_xticks(range(len(top_ratio)))
    ax4.set_xticklabels([name[:10] for name in top_ratio['player_name']], rotation=45)
    
    plt.tight_layout()
    plt.savefig('plots/goal_analysis_detailed.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✅ Saved: plots/goal_analysis_detailed.png")

def generate_final_summary(key_stats, top_scorer, top_team, team_stats):
    """Generate final tournament summary"""
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
    print("📊 Ready for Streamlit Dashboard Development")

def main():
    """Main analysis function"""
    print("🚀 Starting UEFA Champions League 2021-22 EDA Analysis...")
    
    # Load and clean data
    print("\n📥 Loading data...")
    dfs = load_data()
    
    if not dfs:
        print("❌ No data loaded. Exiting.")
        return
    
    print("\n🧹 Cleaning data...")
    clean_dfs = clean_data(dfs)
    
    # Main analysis
    key_stats = clean_dfs['key_stats']
    goals_df = clean_dfs['goals']
    
    # Basic statistics
    teams = analyze_basic_stats(key_stats)
    
    # Top scorers analysis
    top_scorer, top_scorers = analyze_top_scorers(key_stats)
    create_top_scorers_plot(key_stats)
    
    # Team performance
    team_stats, top_team = analyze_team_performance(key_stats)
    create_team_goals_plot(team_stats)
    
    # Goals vs Assists
    create_goals_assists_plot(key_stats)
    
    # Position analysis
    position_stats = analyze_positions(key_stats)
    create_position_plot(key_stats)
    
    # Goal types analysis
    goal_stats = analyze_goal_types(goals_df)
    create_goal_analysis_plot(goals_df, goal_stats)
    
    # Final summary
    generate_final_summary(key_stats, top_scorer, top_team, team_stats)

if __name__ == "__main__":
    main() 