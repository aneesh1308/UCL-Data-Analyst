from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
import json
import os
from django.conf import settings
import csv
import random
from collections import defaultdict, Counter
import warnings
import math
warnings.filterwarnings('ignore')

def load_data():
    """Load and clean all datasets using basic Python"""
    try:
        # Construct data file paths
        data_dir = os.path.join(settings.BASE_DIR, 'data')
        
        data = {}
        
        # Load CSV files using basic Python
        csv_files = ['key_stats.csv', 'goals.csv', 'attacking.csv', 'defending.csv', 
                    'goalkeeping.csv', 'disciplinary.csv', 'attempts.csv']
        
        for csv_file in csv_files:
            file_path = os.path.join(data_dir, csv_file)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    data[csv_file.replace('.csv', '')] = list(reader)
            else:
                data[csv_file.replace('.csv', '')] = []
        
        # Clean and process key_stats data
        for player in data.get('key_stats', []):
            # Clean numeric fields
            for field in ['goals', 'assists', 'minutes_played', 'match_played']:
                try:
                    player[field] = int(player.get(field, 0))
                except (ValueError, TypeError):
                    player[field] = 0
            
            # Clean distance_covered
            try:
                distance = str(player.get('distance_covered', '0'))
                # Remove any non-numeric characters except decimal point
                import re
                match = re.search(r'(\d+\.?\d*)', distance)
                player['distance_covered'] = float(match.group(1)) if match else 0.0
            except:
                player['distance_covered'] = 0.0
            
            # Add calculated fields
            player['impact_rating'] = player['goals'] * 2 + player['assists'] * 1.5
            player['estimated_value'] = (player['goals'] * 2.5 + player['assists'] * 1.5 + 
                                       player['minutes_played'] * 0.01) * random.uniform(0.8, 1.2)
            player['performance_rating'] = (player['goals'] * 3 + player['assists'] * 2 + 
                                          player['distance_covered'] * 0.1 + 
                                          player['minutes_played'] * 0.01) / 5
            
            # Add simulated fields for enhanced analytics
            player['nationality'] = random.choice(['Spain', 'France', 'Germany', 'Brazil', 'Argentina', 
                                                 'England', 'Italy', 'Portugal', 'Netherlands', 'Belgium'])
            player['yellow_cards'] = random.randint(0, 5)
            player['red_cards'] = random.randint(0, 1)
            player['shots_on_target'] = random.randint(0, player['goals'] * 3 + 5)
            player['shots_total'] = player['shots_on_target'] + random.randint(0, 15)
            player['pass_accuracy'] = random.uniform(75, 95)
            player['dribbles_successful'] = random.randint(0, 20)
            player['tackles_won'] = random.randint(0, 15)
            player['interceptions'] = random.randint(0, 10)
            player['age'] = random.randint(18, 35)
            player['height'] = random.randint(165, 200)
            player['weight'] = random.randint(60, 95)
        
        print(f"Loaded {len(data.get('key_stats', []))} players from key_stats.csv")
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def calculate_advanced_stats(data):
    """Calculate advanced statistics using basic Python"""
    key_stats = data.get('key_stats', [])
    
    if not key_stats:
        print("No key_stats data found")
        return {}
    
    print(f"Processing {len(key_stats)} players for advanced stats")
    
    # Basic tournament stats
    total_goals = sum(player['goals'] for player in key_stats)
    total_assists = sum(player['assists'] for player in key_stats)
    total_players = len(key_stats)
    
    # Get unique clubs
    clubs = list(set(player.get('club', '') for player in key_stats if player.get('club')))
    total_teams = len(clubs)
    
    # Calculate team stats
    team_goals = defaultdict(int)
    for player in key_stats:
        team_goals[player.get('club', '')] += player['goals']
    
    avg_goals_per_team = round(sum(team_goals.values()) / len(team_goals) if team_goals else 0, 1)
    avg_impact_rating = round((total_goals + total_assists) / total_players if total_players else 0, 1)
    total_estimated_value = round(sum(p['estimated_value'] for p in key_stats), 0)
    
    tournament_stats = {
        'total_players': total_players,
        'total_teams': total_teams,
        'total_goals': total_goals,
        'total_assists': total_assists,
        'avg_goals_per_team': avg_goals_per_team,
        'avg_impact_rating': avg_impact_rating,
        'total_estimated_value': total_estimated_value
    }
    
    # Top performers
    top_scorer = max(key_stats, key=lambda x: x['goals']) if key_stats else {}
    top_assister = max(key_stats, key=lambda x: x['assists']) if key_stats else {}
    top_impact = max(key_stats, key=lambda x: x['impact_rating']) if key_stats else {}
    
    # Player clustering (AI simulation)
    player_clusters = {
        'Goal Scorers': len([p for p in key_stats if p['goals'] > 5]),
        'Playmakers': len([p for p in key_stats if p['assists'] > 3]),
        'Workhorses': len([p for p in key_stats if p['distance_covered'] > 80]),
        'Defenders': len([p for p in key_stats if p['goals'] <= 2 and p['assists'] <= 2]),
        'All-rounders': len([p for p in key_stats if p['goals'] > 2 and p['assists'] > 2])
    }
    
    # Injury risk assessment (simulated)
    injury_risk_breakdown = {
        'Low': len([p for p in key_stats if p['minutes_played'] < 600]),
        'Medium': len([p for p in key_stats if 600 <= p['minutes_played'] < 900]),
        'High': len([p for p in key_stats if 900 <= p['minutes_played'] < 1200]),
        'Critical': len([p for p in key_stats if p['minutes_played'] >= 1200])
    }
    
    print(f"Tournament stats calculated: {tournament_stats}")
    
    return {
        'tournament_stats': tournament_stats,
        'top_scorer': top_scorer,
        'top_assister': top_assister,
        'top_impact': top_impact,
        'player_clusters': player_clusters,
        'injury_risk_breakdown': injury_risk_breakdown,
        'key_stats': key_stats
    }

def calculate_ai_analytics(data):
    """Calculate AI-powered analytics and predictions"""
    key_stats = data.get('key_stats', [])
    
    if not key_stats:
        return {}
    
    print(f"Calculating AI analytics for {len(key_stats)} players")
    
    # AI Player Clustering (simulated ML)
    ai_clusters = {
        'Star Players': len([p for p in key_stats if p['goals'] > 8 or p['assists'] > 6]),
        'Goal Machines': len([p for p in key_stats if p['goals'] > 5 and p['assists'] <= 3]),
        'Creative Playmakers': len([p for p in key_stats if p['assists'] > 4 and p['goals'] <= 5]),
        'Consistent Performers': len([p for p in key_stats if 2 <= p['goals'] <= 5 and 1 <= p['assists'] <= 4]),
        'Emerging Talents': len([p for p in key_stats if p['goals'] <= 2 and p['assists'] <= 2 and p['distance_covered'] > 60])
    }
    
    # Market Value Analysis
    total_market_value = sum(p['estimated_value'] for p in key_stats)
    avg_market_value = total_market_value / len(key_stats) if key_stats else 0
    
    # Find undervalued gems (high performance, lower market value)
    undervalued_gems = []
    for player in key_stats:
        if player['performance_rating'] > avg_market_value * 0.1 and player['estimated_value'] < avg_market_value:
            undervalued_gems.append(player)
    
    market_analysis = {
        'total_market_value': total_market_value,
        'avg_market_value': avg_market_value,
        'most_valuable': max(key_stats, key=lambda x: x['estimated_value']) if key_stats else {},
        'undervalued_gems': sorted(undervalued_gems, key=lambda x: x['performance_rating'], reverse=True)[:8]
    }
    
    # Performance Predictions (simulated ML predictions)
    for player in key_stats:
        # Simulate next season prediction based on current performance
        current_performance = player['goals'] + player['assists']
        trend_factor = random.uniform(0.8, 1.3)  # Performance can vary ±30%
        player['predicted_performance'] = current_performance * trend_factor
        player['goal_contribution'] = player['goals'] + player['assists']
    
    top_prospects = sorted(key_stats, key=lambda x: x['predicted_performance'], reverse=True)[:20]
    
    # Injury Risk Analysis (simulated AI model)
    injury_risk_stats = {'Low': 0, 'Medium': 0, 'High': 0, 'Critical': 0}
    for player in key_stats:
        minutes_avg = player['minutes_played'] / max(player['match_played'], 1)  # Average per match
        if minutes_avg < 60:
            risk = 'Low'
        elif minutes_avg < 80:
            risk = 'Medium'
        elif minutes_avg < 90:
            risk = 'High'
        else:
            risk = 'Critical'
        
        player['injury_risk'] = risk
        injury_risk_stats[risk] += 1
    
    print(f"AI clusters: {ai_clusters}")
    print(f"Market analysis: Total value ${total_market_value:.0f}M, Undervalued gems: {len(undervalued_gems)}")
    
    return {
        'player_clusters': ai_clusters,
        'market_analysis': market_analysis,
        'top_prospects': top_prospects,
        'injury_risk_stats': injury_risk_stats,
        'total_tournament_stats': calculate_advanced_stats(data)['tournament_stats']
    }

def calculate_team_analytics(data):
    """Calculate comprehensive team analytics"""
    key_stats = data.get('key_stats', [])
    
    if not key_stats:
        return {}
    
    print(f"Calculating team analytics for {len(key_stats)} players")
    
    # Group by teams with comprehensive stats
    teams_data = defaultdict(lambda: {
        'club': '',
        'players': 0,
        'goals': 0,
        'assists': 0,
        'yellow_cards': 0,
        'red_cards': 0,
        'total_distance': 0,
        'avg_performance': 0,
        'total_minutes': 0,
        'country': '',
        'played': 0,
        'won': 0,
        'drawn': 0,
        'lost': 0,
        'goals_for': 0,
        'goals_against': 0,
        'points': 0
    })
    
    countries = ['Spain', 'England', 'Germany', 'France', 'Italy', 'Portugal', 'Netherlands', 'Belgium']
    
    for player in key_stats:
        club = player.get('club', 'Unknown')
        teams_data[club]['club'] = club
        teams_data[club]['players'] += 1
        teams_data[club]['goals'] += player['goals']
        teams_data[club]['assists'] += player['assists']
        teams_data[club]['yellow_cards'] += player['yellow_cards']
        teams_data[club]['red_cards'] += player['red_cards']
        teams_data[club]['total_distance'] += player['distance_covered']
        teams_data[club]['avg_performance'] += player['performance_rating']
        teams_data[club]['total_minutes'] += player['minutes_played']
    
    # Convert to list and add calculated fields
    teams_list = []
    for team_data in teams_data.values():
        if team_data['players'] > 0:  # Only include teams with players
            team_data['total_contributions'] = team_data['goals'] + team_data['assists']
            team_data['avg_performance'] = team_data['avg_performance'] / team_data['players']
            team_data['possession'] = random.uniform(45, 65)  # Simulated possession %
            
            # Simulate additional team stats based on player performance
            team_data['country'] = random.choice(countries)
            team_data['played'] = random.randint(6, 13)
            team_data['won'] = min(random.randint(2, 10), team_data['played'])
            team_data['drawn'] = min(random.randint(0, 4), team_data['played'] - team_data['won'])
            team_data['lost'] = team_data['played'] - team_data['won'] - team_data['drawn']
            team_data['goals_for'] = team_data['goals'] + random.randint(5, 15)
            team_data['goals_against'] = random.randint(3, 20)
            team_data['points'] = team_data['won'] * 3 + team_data['drawn']
            
            teams_list.append(team_data)
    
    # Sort by total contributions
    teams_list.sort(key=lambda x: x['total_contributions'], reverse=True)
    
    # Team categories and insights
    champion = max(teams_list, key=lambda x: x['points']) if teams_list else {}
    top_scorer_team = max(teams_list, key=lambda x: x['goals']) if teams_list else {}
    best_defense = min(teams_list, key=lambda x: x['goals_against']) if teams_list else {}
    highest_possession = max(teams_list, key=lambda x: x['possession']) if teams_list else {}
    
    # Team insights
    team_insights = [
        {
            'title': 'Attacking Powerhouse',
            'description': f"{top_scorer_team.get('club', 'N/A')} leads with {top_scorer_team.get('goals', 0)} goals",
            'impact': 'High'
        },
        {
            'title': 'Defensive Wall',
            'description': f"{best_defense.get('club', 'N/A')} conceded only {best_defense.get('goals_against', 0)} goals",
            'impact': 'High'
        },
        {
            'title': 'Ball Control Masters',
            'description': f"{highest_possession.get('club', 'N/A')} dominates possession",
            'impact': 'Medium'
        }
    ]
    
    print(f"Processed {len(teams_list)} teams")
    
    return {
        'teams': teams_list,
        'champion': champion,
        'top_scorer_team': top_scorer_team,
        'best_defense': best_defense,
        'highest_possession': highest_possession,
        'team_insights': team_insights,
        'impact_teams': teams_list[:4]  # Top 4 teams for impact display
    }

def calculate_player_analytics(data):
    """Calculate comprehensive player analytics"""
    key_stats = data.get('key_stats', [])
    
    if not key_stats:
        return {}
    
    print(f"Calculating player analytics for {len(key_stats)} players")
    
    # Position-based analysis
    position_stats = defaultdict(lambda: {
        'total_players': 0,
        'avg_rating': 0,
        'total_goals': 0,
        'total_assists': 0
    })
    
    for player in key_stats:
        pos = player.get('position', 'Unknown')
        position_stats[pos]['total_players'] += 1
        position_stats[pos]['avg_rating'] += player['performance_rating']
        position_stats[pos]['total_goals'] += player['goals']
        position_stats[pos]['total_assists'] += player['assists']
    
    # Calculate averages
    for pos_data in position_stats.values():
        if pos_data['total_players'] > 0:
            pos_data['avg_rating'] /= pos_data['total_players']
    
    # Top performers
    top_performers = sorted(key_stats, key=lambda x: x['performance_rating'], reverse=True)[:10]
    
    # MVP calculation
    mvp = max(key_stats, key=lambda x: x['impact_rating']) if key_stats else {}
    mvp['impact_score'] = mvp.get('impact_rating', 0)
    
    avg_performance = sum(p['performance_rating'] for p in key_stats) / len(key_stats) if key_stats else 0
    
    print(f"Top performer: {top_performers[0]['player_name'] if top_performers else 'None'}")
    print(f"MVP: {mvp.get('player_name', 'None')}")
    
    return {
        'total_players': len(key_stats),
        'top_scorer': max(key_stats, key=lambda x: x['goals']) if key_stats else {},
        'mvp': mvp,
        'avg_performance': avg_performance,
        'position_stats': dict(position_stats),
        'top_performers': top_performers,
        'player_stats': key_stats
    }

def create_chart_data(data):
    """Create Chart.js compatible data for visualizations"""
    key_stats = data.get('key_stats', [])
    
    if not key_stats:
        return {}
    
    print(f"Creating chart data for {len(key_stats)} players")
    
    # Goals by Position Chart
    position_goals = defaultdict(int)
    for player in key_stats:
        position = player.get('position', 'Unknown')
        position_goals[position] += player['goals']
    
    position_chart = {
        'labels': list(position_goals.keys()),
        'datasets': [{
            'data': list(position_goals.values()),
            'backgroundColor': [
                '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
                '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9'
            ]
        }]
    }
    
    # Top Teams Performance Chart
    team_stats = defaultdict(lambda: {'goals': 0, 'assists': 0})
    for player in key_stats:
        club = player.get('club', 'Unknown')
        team_stats[club]['goals'] += player['goals']
        team_stats[club]['assists'] += player['assists']
    
    # Get top 10 teams
    top_teams = sorted(team_stats.items(), key=lambda x: x[1]['goals'] + x[1]['assists'], reverse=True)[:10]
    
    teams_chart = {
        'labels': [team[0] for team in top_teams],
        'datasets': [
            {
                'label': 'Goals',
                'data': [team[1]['goals'] for team in top_teams],
                'backgroundColor': '#FF6B6B'
            },
            {
                'label': 'Assists',
                'data': [team[1]['assists'] for team in top_teams],
                'backgroundColor': '#4ECDC4'
            }
        ]
    }
    
    # Goal Progression Trends Chart (NEW)
    # Simulate tournament progression data
    match_days = ['Group Stage', 'Round of 16', 'Quarter Finals', 'Semi Finals', 'Final']
    goals_progression = [120, 85, 45, 25, 8]  # Simulated goals per stage
    assists_progression = [95, 68, 35, 20, 6]  # Simulated assists per stage
    
    trends_chart = {
        'labels': match_days,
        'datasets': [
            {
                'label': 'Goals',
                'data': goals_progression,
                'borderColor': '#FF6B6B',
                'backgroundColor': 'rgba(255, 107, 107, 0.1)',
                'tension': 0.4,
                'fill': True
            },
            {
                'label': 'Assists',
                'data': assists_progression,
                'borderColor': '#4ECDC4',
                'backgroundColor': 'rgba(78, 205, 196, 0.1)',
                'tension': 0.4,
                'fill': True
            }
        ]
    }
    
    # Player Performance Chart (for players page)
    top_players = sorted(key_stats, key=lambda x: x.get('performance_rating', 0), reverse=True)[:15]
    
    performance_chart = {
        'labels': [p.get('player_name', 'Unknown')[:15] + '...' if len(p.get('player_name', '')) > 15 else p.get('player_name', 'Unknown') for p in top_players],
        'datasets': [{
            'label': 'Performance Rating',
            'data': [p.get('performance_rating', 0) for p in top_players],
            'backgroundColor': '#45B7D1'
        }]
    }
    
    # Team Rankings Chart (for teams page)
    team_analytics = calculate_team_analytics(data)
    top_ranked_teams = sorted(team_analytics.get('teams', []), key=lambda x: x['points'], reverse=True)[:10]
    
    rankings_chart = {
        'labels': [team['club'] for team in top_ranked_teams],
        'datasets': [{
            'label': 'Points',
            'data': [team['points'] for team in top_ranked_teams],
            'backgroundColor': '#96CEB4'
        }]
    }
    
    # AI Clusters Chart (for advanced analytics)
    ai_analytics = calculate_ai_analytics(data)
    clusters = ai_analytics.get('player_clusters', {})
    
    clusters_chart = {
        'labels': list(clusters.keys()),
        'datasets': [{
            'data': list(clusters.values()),
            'backgroundColor': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        }]
    }
    
    # Injury Risk Chart
    injury_data = ai_analytics.get('injury_risk_stats', {})
    
    injury_chart = {
        'labels': list(injury_data.keys()),
        'datasets': [{
            'data': list(injury_data.values()),
            'backgroundColor': ['#4ECDC4', '#FFEAA7', '#FF6B6B', '#E17055']
        }]
    }
    
    print("Chart data created successfully")
    
    return {
        'position_chart': json.dumps(position_chart),
        'teams_chart': json.dumps(teams_chart),
        'trends_chart': json.dumps(trends_chart),
        'performance_chart': json.dumps(performance_chart),
        'rankings_chart': json.dumps(rankings_chart),
        'clusters_chart': json.dumps(clusters_chart),
        'injury_chart': json.dumps(injury_chart)
    }

def overview(request):
    """Overview page with comprehensive analytics"""
    try:
        print("Loading overview page...")
        data = load_data()
        if data is None:
            context = {'error': 'Failed to load data'}
        else:
            stats = calculate_advanced_stats(data)
            charts = create_chart_data(data)
            
            context = {
                **stats,
                **charts,
                'page_title': 'UEFA Champions League Analytics - Overview'
            }
            print(f"Overview context keys: {list(context.keys())}")
    except Exception as e:
        print(f"Error in overview: {e}")
        context = {'error': f'Error: {str(e)}'}
    
    return render(request, 'dashboard/overview.html', context)

def players(request):
    """Players page with detailed analysis"""
    try:
        print("Loading players page...")
        data = load_data()
        if data is None:
            context = {'error': 'Failed to load data'}
        else:
            player_analytics = calculate_player_analytics(data)
            charts = create_chart_data(data)
            
            context = {
                **player_analytics,
                'performance_chart': charts.get('performance_chart'),
                'position_chart': charts.get('position_chart'),
                'page_title': 'Players Analysis'
            }
            print(f"Players context keys: {list(context.keys())}")
            print(f"Total players: {context.get('total_players', 0)}")
    except Exception as e:
        print(f"Error in players: {e}")
        context = {'error': f'Error: {str(e)}'}
    
    return render(request, 'dashboard/players.html', context)

def teams(request):
    """Teams page with team analysis"""
    try:
        print("Loading teams page...")
        data = load_data()
        if data is None:
            context = {'error': 'Failed to load data'}
        else:
            team_analytics = calculate_team_analytics(data)
            charts = create_chart_data(data)
            
            context = {
                **team_analytics,
                'rankings_chart': charts.get('rankings_chart'),
                'teams_chart': charts.get('teams_chart'),
                'team_stats': team_analytics['teams'],
                'page_title': 'Teams Analysis'
            }
            print(f"Teams context keys: {list(context.keys())}")
            print(f"Total teams: {len(context.get('teams', []))}")
    except Exception as e:
        print(f"Error in teams: {e}")
        context = {'error': f'Error: {str(e)}'}
    
    return render(request, 'dashboard/teams.html', context)

def goals(request):
    """Goals analysis page"""
    try:
        print("Loading goals page...")
        data = load_data()
        if data is None:
            context = {'error': 'Failed to load data'}
        else:
            goals_data = data.get('goals', [])
            key_stats = data.get('key_stats', [])
            
            # Top scorers
            top_scorers = sorted(key_stats, key=lambda x: x['goals'], reverse=True)[:10]
            
            context = {
                'goals': goals_data,
                'top_scorers': top_scorers,
                'page_title': 'Goals Analysis'
            }
            print(f"Goals context: {len(top_scorers)} top scorers")
    except Exception as e:
        print(f"Error in goals: {e}")
        context = {'error': f'Error: {str(e)}'}
    
    return render(request, 'dashboard/goals.html', context)

def advanced_analytics(request):
    """Advanced analytics with AI insights"""
    try:
        print("Loading advanced analytics page...")
        data = load_data()
        if data is None:
            context = {'error': 'Failed to load data'}
        else:
            ai_analytics = calculate_ai_analytics(data)
            charts = create_chart_data(data)
            
            context = {
                **ai_analytics,
                'insights': ai_analytics,
                'clusters_chart': charts.get('clusters_chart'),
                'injury_chart': charts.get('injury_chart'),
                'page_title': 'Advanced Analytics'
            }
            print(f"Advanced analytics context keys: {list(context.keys())}")
            print(f"AI clusters: {ai_analytics.get('player_clusters', {})}")
    except Exception as e:
        print(f"Error in advanced_analytics: {e}")
        context = {'error': f'Error: {str(e)}'}
    
    return render(request, 'dashboard/advanced_analytics.html', context)

def tactical_analysis(request):
    """Tactical analysis page"""
    try:
        data = load_data()
        if data is None:
            context = {'error': 'Failed to load data'}
        else:
            stats = calculate_advanced_stats(data)
            charts = create_chart_data(data)
            
            context = {
                **stats,
                **charts,
                'page_title': 'Tactical Analysis'
            }
    except Exception as e:
        context = {'error': f'Error: {str(e)}'}
    
    return render(request, 'dashboard/tactical_analysis.html', context)

# API endpoints
def get_player_data(request, player_name):
    """Get individual player data"""
    try:
        data = load_data()
        if data is None:
            return JsonResponse({'error': 'Failed to load data'})
        
        key_stats = data.get('key_stats', [])
        player_data = None
        
        for player in key_stats:
            if player.get('player_name', '').lower() == player_name.lower():
                player_data = player
                break
        
        if player_data:
            return JsonResponse({'player': player_data})
        else:
            return JsonResponse({'error': 'Player not found'})
    
    except Exception as e:
        return JsonResponse({'error': str(e)})

def get_team_data(request, team_name):
    """Get team data"""
    try:
        data = load_data()
        if data is None:
            return JsonResponse({'error': 'Failed to load data'})
        
        key_stats = data.get('key_stats', [])
        team_players = []
        
        for player in key_stats:
            if player.get('club', '').lower() == team_name.lower():
                team_players.append(player)
        
        if team_players:
            return JsonResponse({'team': team_name, 'players': team_players})
        else:
            return JsonResponse({'error': 'Team not found'})
    
    except Exception as e:
        return JsonResponse({'error': str(e)})

# Test endpoints
def test_view(request):
    """Simple test view"""
    return HttpResponse("Django is working! Test successful.")

def test_data_view(request):
    """Test data loading"""
    try:
        data = load_data()
        if data is None:
            return HttpResponse("Error: Data loading failed")
        
        info = {}
        for key, data_list in data.items():
            info[key] = f"Records: {len(data_list)}"
        
        return HttpResponse(f"Data loading successful! Info: {info}")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")

def comprehensive_dashboard(request):
    """Comprehensive Streamlit-style dashboard with all analytics"""
    try:
        print("Loading comprehensive dashboard...")
        data = load_data()
        if data is None:
            context = {'error': 'Failed to load data'}
        else:
            # Get all analytics
            basic_stats = calculate_advanced_stats(data)
            ai_analytics = calculate_ai_analytics(data)
            team_analytics = calculate_team_analytics(data)
            player_analytics = calculate_player_analytics(data)
            charts = create_chart_data(data)
            
            # Additional comprehensive analytics
            key_stats = data.get('key_stats', [])
            
            # Performance distribution analysis
            performance_distribution = {
                'Excellent (>15)': len([p for p in key_stats if p['performance_rating'] > 15]),
                'Good (10-15)': len([p for p in key_stats if 10 <= p['performance_rating'] <= 15]),
                'Average (5-10)': len([p for p in key_stats if 5 <= p['performance_rating'] < 10]),
                'Below Average (<5)': len([p for p in key_stats if p['performance_rating'] < 5])
            }
            
            # Age group analysis (simulated)
            age_groups = {
                'Young (18-23)': len([p for p in key_stats if p['minutes_played'] < 500]),
                'Prime (24-29)': len([p for p in key_stats if 500 <= p['minutes_played'] < 1000]),
                'Experienced (30+)': len([p for p in key_stats if p['minutes_played'] >= 1000])
            }
            
            # Position effectiveness
            position_effectiveness = {}
            for player in key_stats:
                pos = player.get('position', 'Unknown')
                if pos not in position_effectiveness:
                    position_effectiveness[pos] = {
                        'total_players': 0,
                        'total_goals': 0,
                        'total_assists': 0,
                        'avg_performance': 0,
                        'effectiveness_score': 0
                    }
                position_effectiveness[pos]['total_players'] += 1
                position_effectiveness[pos]['total_goals'] += player['goals']
                position_effectiveness[pos]['total_assists'] += player['assists']
                position_effectiveness[pos]['avg_performance'] += player['performance_rating']
            
            # Calculate effectiveness scores
            for pos_data in position_effectiveness.values():
                if pos_data['total_players'] > 0:
                    pos_data['avg_performance'] /= pos_data['total_players']
                    pos_data['effectiveness_score'] = (
                        pos_data['total_goals'] * 2 + 
                        pos_data['total_assists'] * 1.5 + 
                        pos_data['avg_performance']
                    ) / pos_data['total_players']
            
            # Top performers by category
            top_categories = {
                'goal_scorers': sorted(key_stats, key=lambda x: x['goals'], reverse=True)[:5],
                'assist_leaders': sorted(key_stats, key=lambda x: x['assists'], reverse=True)[:5],
                'distance_runners': sorted(key_stats, key=lambda x: x['distance_covered'], reverse=True)[:5],
                'most_valuable': sorted(key_stats, key=lambda x: x['estimated_value'], reverse=True)[:5],
                'best_performers': sorted(key_stats, key=lambda x: x['performance_rating'], reverse=True)[:5]
            }
            
            # Team comparison metrics
            teams = team_analytics.get('teams', [])
            team_comparison = {
                'most_goals': max(teams, key=lambda x: x['goals']) if teams else {},
                'most_assists': max(teams, key=lambda x: x['assists']) if teams else {},
                'best_defense': min(teams, key=lambda x: x['goals_against']) if teams else {},
                'highest_possession': max(teams, key=lambda x: x['possession']) if teams else {},
                'most_disciplined': min(teams, key=lambda x: x['yellow_cards'] + x['red_cards']) if teams else {}
            }
            
            # Statistical insights
            statistical_insights = {
                'total_matches_played': sum(p['match_played'] for p in key_stats),
                'total_minutes': sum(p['minutes_played'] for p in key_stats),
                'total_distance': sum(p['distance_covered'] for p in key_stats),
                'avg_goals_per_player': sum(p['goals'] for p in key_stats) / len(key_stats) if key_stats else 0,
                'avg_assists_per_player': sum(p['assists'] for p in key_stats) / len(key_stats) if key_stats else 0,
                'goals_per_minute': (sum(p['goals'] for p in key_stats) / sum(p['minutes_played'] for p in key_stats)) * 90 if sum(p['minutes_played'] for p in key_stats) > 0 else 0,
                'most_active_position': max(position_effectiveness.items(), key=lambda x: x[1]['total_players'])[0] if position_effectiveness else 'Unknown'
            }
            
            # Create additional charts for comprehensive dashboard
            comprehensive_charts = {
                # Performance distribution chart
                'performance_dist_chart': json.dumps({
                    'labels': list(performance_distribution.keys()),
                    'datasets': [{
                        'data': list(performance_distribution.values()),
                        'backgroundColor': ['#4ECDC4', '#45B7D1', '#FFEAA7', '#FF6B6B']
                    }]
                }),
                
                # Age groups chart
                'age_groups_chart': json.dumps({
                    'labels': list(age_groups.keys()),
                    'datasets': [{
                        'data': list(age_groups.values()),
                        'backgroundColor': ['#96CEB4', '#45B7D1', '#DDA0DD']
                    }]
                }),
                
                # Position effectiveness chart
                'position_effectiveness_chart': json.dumps({
                    'labels': list(position_effectiveness.keys()),
                    'datasets': [{
                        'label': 'Effectiveness Score',
                        'data': [pos['effectiveness_score'] for pos in position_effectiveness.values()],
                        'backgroundColor': '#FF6B6B'
                    }]
                }),
                
                # Goals vs Assists scatter
                'goals_assists_scatter': json.dumps({
                    'datasets': [{
                        'label': 'Players',
                        'data': [{'x': p['goals'], 'y': p['assists']} for p in key_stats[:50]],
                        'backgroundColor': '#45B7D1'
                    }]
                })
            }
            
            context = {
                # Basic analytics
                **basic_stats,
                **ai_analytics,
                **team_analytics,
                **player_analytics,
                **charts,
                **comprehensive_charts,
                
                # Additional comprehensive data
                'performance_distribution': performance_distribution,
                'age_groups': age_groups,
                'position_effectiveness': position_effectiveness,
                'top_categories': top_categories,
                'team_comparison': team_comparison,
                'statistical_insights': statistical_insights,
                'page_title': 'Comprehensive Analytics Dashboard'
            }
            
            print(f"Comprehensive dashboard loaded with {len(context)} data points")
            
    except Exception as e:
        print(f"Error in comprehensive_dashboard: {e}")
        context = {'error': f'Error: {str(e)}'}
    
    return render(request, 'dashboard/comprehensive_dashboard.html', context)

def generate_match_data():
    """Generate simulated match data for the tournament"""
    teams = ['Real Madrid', 'Manchester City', 'Liverpool', 'Bayern Munich', 'PSG', 'Chelsea', 
             'Barcelona', 'Atletico Madrid', 'Juventus', 'Inter Milan', 'AC Milan', 'Napoli',
             'Borussia Dortmund', 'RB Leipzig', 'Ajax', 'Benfica', 'Porto', 'Sporting CP',
             'Sevilla', 'Villarreal', 'Manchester United', 'Arsenal', 'Tottenham', 'Leicester',
             'Atalanta', 'Roma', 'Lazio', 'Fiorentina', 'Valencia', 'Real Sociedad', 'Betis', 'Salzburg']
    
    stages = ['Group Stage', 'Round of 16', 'Quarter Finals', 'Semi Finals', 'Final']
    
    matches = []
    match_id = 1
    
    # Generate matches for each stage
    for stage in stages:
        if stage == 'Group Stage':
            num_matches = 48  # 8 groups × 6 matches
        elif stage == 'Round of 16':
            num_matches = 16
        elif stage == 'Quarter Finals':
            num_matches = 8
        else:  # Final
            num_matches = 2  # Final + 3rd place playoff
        
        for i in range(num_matches):
            home_team = random.choice(teams)
            away_team = random.choice([t for t in teams if t != home_team])
            
            home_goals = random.randint(0, 4)
            away_goals = random.randint(0, 4)
            
            # Adjust for knockout stages (less draws)
            if stage != 'Group Stage' and home_goals == away_goals:
                if random.choice([True, False]):
                    home_goals += 1
                else:
                    away_goals += 1
            
            match = {
                'match_id': match_id,
                'stage': stage,
                'home_team': home_team,
                'away_team': away_team,
                'home_goals': home_goals,
                'away_goals': away_goals,
                'total_goals': home_goals + away_goals,
                'result': 'Home Win' if home_goals > away_goals else 'Away Win' if away_goals > home_goals else 'Draw',
                'attendance': random.randint(40000, 80000),
                'possession_home': random.randint(35, 65),
                'shots_home': random.randint(5, 20),
                'shots_away': random.randint(5, 20),
                'corners_home': random.randint(2, 12),
                'corners_away': random.randint(2, 12),
                'fouls_home': random.randint(8, 20),
                'fouls_away': random.randint(8, 20),
                'yellow_cards_home': random.randint(0, 5),
                'yellow_cards_away': random.randint(0, 5),
                'red_cards_home': random.randint(0, 1),
                'red_cards_away': random.randint(0, 1),
                'date': f"2021-{random.randint(9, 12):02d}-{random.randint(1, 28):02d}"
            }
            match['possession_away'] = 100 - match['possession_home']
            matches.append(match)
            match_id += 1
    
    return matches

def matches(request):
    """Comprehensive matches analysis page"""
    try:
        print("Loading matches page...")
        data = load_data()
        if data is None:
            context = {'error': 'Failed to load data'}
        else:
            # Generate match data
            matches_data = generate_match_data()
            
            # Calculate match statistics
            total_matches = len(matches_data)
            total_goals = sum(match['total_goals'] for match in matches_data)
            avg_goals_per_match = total_goals / total_matches if total_matches > 0 else 0
            
            # Stage-wise analysis
            stage_stats = defaultdict(lambda: {
                'matches': 0, 'goals': 0, 'avg_goals': 0, 'home_wins': 0, 
                'away_wins': 0, 'draws': 0, 'avg_attendance': 0
            })
            
            for match in matches_data:
                stage = match['stage']
                stage_stats[stage]['matches'] += 1
                stage_stats[stage]['goals'] += match['total_goals']
                stage_stats[stage]['avg_attendance'] += match['attendance']
                
                if match['result'] == 'Home Win':
                    stage_stats[stage]['home_wins'] += 1
                elif match['result'] == 'Away Win':
                    stage_stats[stage]['away_wins'] += 1
                else:
                    stage_stats[stage]['draws'] += 1
            
            # Calculate averages
            for stage_data in stage_stats.values():
                if stage_data['matches'] > 0:
                    stage_data['avg_goals'] = stage_data['goals'] / stage_data['matches']
                    stage_data['avg_attendance'] = stage_data['avg_attendance'] / stage_data['matches']
            
            # Top matches by goals
            top_scoring_matches = sorted(matches_data, key=lambda x: x['total_goals'], reverse=True)[:10]
            
            # Team performance in matches
            team_match_stats = defaultdict(lambda: {
                'matches': 0, 'wins': 0, 'draws': 0, 'losses': 0, 
                'goals_for': 0, 'goals_against': 0, 'points': 0
            })
            
            for match in matches_data:
                home_team = match['home_team']
                away_team = match['away_team']
                
                # Home team stats
                team_match_stats[home_team]['matches'] += 1
                team_match_stats[home_team]['goals_for'] += match['home_goals']
                team_match_stats[home_team]['goals_against'] += match['away_goals']
                
                # Away team stats
                team_match_stats[away_team]['matches'] += 1
                team_match_stats[away_team]['goals_for'] += match['away_goals']
                team_match_stats[away_team]['goals_against'] += match['home_goals']
                
                # Results
                if match['result'] == 'Home Win':
                    team_match_stats[home_team]['wins'] += 1
                    team_match_stats[home_team]['points'] += 3
                    team_match_stats[away_team]['losses'] += 1
                elif match['result'] == 'Away Win':
                    team_match_stats[away_team]['wins'] += 1
                    team_match_stats[away_team]['points'] += 3
                    team_match_stats[home_team]['losses'] += 1
                else:
                    team_match_stats[home_team]['draws'] += 1
                    team_match_stats[home_team]['points'] += 1
                    team_match_stats[away_team]['draws'] += 1
                    team_match_stats[away_team]['points'] += 1
            
            # Convert to list and sort by points
            team_standings = []
            for team, stats in team_match_stats.items():
                stats['team'] = team
                stats['goal_difference'] = stats['goals_for'] - stats['goals_against']
                team_standings.append(stats)
            
            team_standings.sort(key=lambda x: (x['points'], x['goal_difference']), reverse=True)
            
            # Match insights
            match_insights = [
                {
                    'title': 'High-Scoring Tournament',
                    'description': f'Average of {avg_goals_per_match:.1f} goals per match',
                    'icon': 'fas fa-futbol',
                    'color': 'success'
                },
                {
                    'title': 'Home Advantage',
                    'description': f'{sum(1 for m in matches_data if m["result"] == "Home Win")} home wins vs {sum(1 for m in matches_data if m["result"] == "Away Win")} away wins',
                    'icon': 'fas fa-home',
                    'color': 'info'
                },
                {
                    'title': 'Competitive Balance',
                    'description': f'{sum(1 for m in matches_data if m["result"] == "Draw")} matches ended in draws',
                    'icon': 'fas fa-balance-scale',
                    'color': 'warning'
                }
            ]
            
            context = {
                'matches_data': matches_data[:20],  # Show first 20 matches
                'total_matches': total_matches,
                'total_goals': total_goals,
                'avg_goals_per_match': avg_goals_per_match,
                'stage_stats': dict(stage_stats),
                'top_scoring_matches': top_scoring_matches,
                'team_standings': team_standings[:16],  # Top 16 teams
                'match_insights': match_insights,
                'page_title': 'Matches Analysis'
            }
            print(f"Matches context: {total_matches} matches, {total_goals} goals")
    except Exception as e:
        print(f"Error in matches: {e}")
        context = {'error': f'Error: {str(e)}'}
    
    return render(request, 'dashboard/matches.html', context)

def goals_and_scoring(request):
    """Enhanced goals and scoring analysis page"""
    try:
        print("Loading goals and scoring page...")
        data = load_data()
        if data is None:
            context = {'error': 'Failed to load data'}
        else:
            key_stats = data.get('key_stats', [])
            goals_data = data.get('goals', [])
            
            # Enhanced goal statistics
            total_goals = sum(player['goals'] for player in key_stats)
            total_assists = sum(player['assists'] for player in key_stats)
            total_shots = sum(player['shots_total'] for player in key_stats)
            total_shots_on_target = sum(player['shots_on_target'] for player in key_stats)
            
            # Shooting accuracy
            shooting_accuracy = (total_shots_on_target / total_shots * 100) if total_shots > 0 else 0
            conversion_rate = (total_goals / total_shots_on_target * 100) if total_shots_on_target > 0 else 0
            
            # Top scorers with enhanced stats
            top_scorers = sorted(key_stats, key=lambda x: x['goals'], reverse=True)[:20]
            for scorer in top_scorers:
                scorer['goals_per_match'] = scorer['goals'] / max(scorer['match_played'], 1)
                scorer['shot_accuracy'] = (scorer['shots_on_target'] / max(scorer['shots_total'], 1) * 100)
                scorer['conversion_rate'] = (scorer['goals'] / max(scorer['shots_on_target'], 1) * 100)
            
            # Goals by position analysis
            position_goals = defaultdict(lambda: {'goals': 0, 'players': 0, 'avg_goals': 0})
            for player in key_stats:
                pos = player.get('position', 'Unknown')
                position_goals[pos]['goals'] += player['goals']
                position_goals[pos]['players'] += 1
            
            for pos_data in position_goals.values():
                if pos_data['players'] > 0:
                    pos_data['avg_goals'] = pos_data['goals'] / pos_data['players']
            
            # Goals by team
            team_goals = defaultdict(lambda: {'goals': 0, 'assists': 0, 'players': 0})
            for player in key_stats:
                team = player.get('club', 'Unknown')
                team_goals[team]['goals'] += player['goals']
                team_goals[team]['assists'] += player['assists']
                team_goals[team]['players'] += 1
            
            top_scoring_teams = sorted(team_goals.items(), key=lambda x: x[1]['goals'], reverse=True)[:10]
            
            # Goal scoring patterns
            goal_patterns = {
                'Prolific Scorers (5+ goals)': len([p for p in key_stats if p['goals'] >= 5]),
                'Regular Scorers (2-4 goals)': len([p for p in key_stats if 2 <= p['goals'] <= 4]),
                'Occasional Scorers (1 goal)': len([p for p in key_stats if p['goals'] == 1]),
                'Non-scorers': len([p for p in key_stats if p['goals'] == 0])
            }
            
            # Assist analysis
            top_assisters = sorted(key_stats, key=lambda x: x['assists'], reverse=True)[:15]
            assist_to_goal_ratio = total_assists / total_goals if total_goals > 0 else 0
            
            # Goal scoring insights
            scoring_insights = [
                {
                    'title': 'Clinical Finishing',
                    'description': f'{conversion_rate:.1f}% conversion rate from shots on target',
                    'icon': 'fas fa-crosshairs',
                    'color': 'success'
                },
                {
                    'title': 'Team Play',
                    'description': f'{assist_to_goal_ratio:.1f} assists per goal shows great teamwork',
                    'icon': 'fas fa-hands-helping',
                    'color': 'info'
                },
                {
                    'title': 'Shot Accuracy',
                    'description': f'{shooting_accuracy:.1f}% of shots hit the target',
                    'icon': 'fas fa-bullseye',
                    'color': 'warning'
                }
            ]
            
            context = {
                'total_goals': total_goals,
                'total_assists': total_assists,
                'total_shots': total_shots,
                'total_shots_on_target': total_shots_on_target,
                'shooting_accuracy': shooting_accuracy,
                'conversion_rate': conversion_rate,
                'top_scorers': top_scorers,
                'top_assisters': top_assisters,
                'position_goals': dict(position_goals),
                'top_scoring_teams': top_scoring_teams,
                'goal_patterns': goal_patterns,
                'assist_to_goal_ratio': assist_to_goal_ratio,
                'scoring_insights': scoring_insights,
                'page_title': 'Goals & Scoring Analysis'
            }
            print(f"Goals context: {total_goals} goals, {total_assists} assists")
    except Exception as e:
        print(f"Error in goals_and_scoring: {e}")
        context = {'error': f'Error: {str(e)}'}
    
    return render(request, 'dashboard/goals_scoring.html', context)

def players(request):
    """Enhanced players page with pagination and detailed analytics"""
    try:
        print("Loading enhanced players page...")
        data = load_data()
        if data is None:
            context = {'error': 'Failed to load data'}
        else:
            key_stats = data.get('key_stats', [])
            
            # Get filter parameters
            position_filter = request.GET.get('position', '')
            team_filter = request.GET.get('team', '')
            sort_by = request.GET.get('sort', 'performance_rating')
            
            # Filter players
            filtered_players = key_stats.copy()
            
            if position_filter:
                filtered_players = [p for p in filtered_players if p.get('position', '') == position_filter]
            
            if team_filter:
                filtered_players = [p for p in filtered_players if p.get('club', '') == team_filter]
            
            # Sort players
            if sort_by == 'goals':
                filtered_players.sort(key=lambda x: x['goals'], reverse=True)
            elif sort_by == 'assists':
                filtered_players.sort(key=lambda x: x['assists'], reverse=True)
            elif sort_by == 'minutes_played':
                filtered_players.sort(key=lambda x: x['minutes_played'], reverse=True)
            elif sort_by == 'estimated_value':
                filtered_players.sort(key=lambda x: x['estimated_value'], reverse=True)
            else:  # performance_rating
                filtered_players.sort(key=lambda x: x['performance_rating'], reverse=True)
            
            # Enhanced player statistics
            for player in filtered_players:
                player['goals_per_match'] = player['goals'] / max(player['match_played'], 1)
                player['assists_per_match'] = player['assists'] / max(player['match_played'], 1)
                player['minutes_per_goal'] = player['minutes_played'] / max(player['goals'], 1)
                player['shot_accuracy'] = (player['shots_on_target'] / max(player['shots_total'], 1) * 100)
                player['bmi'] = player['weight'] / ((player['height'] / 100) ** 2)
                player['fitness_score'] = (player['distance_covered'] / max(player['minutes_played'], 1)) * 90
            
            # Pagination
            paginator = Paginator(filtered_players, 20)  # 20 players per page
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            # Get unique values for filters
            positions = sorted(list(set(p.get('position', '') for p in key_stats if p.get('position'))))
            teams = sorted(list(set(p.get('club', '') for p in key_stats if p.get('club'))))
            
            # Player analytics
            total_players = len(key_stats)
            avg_age = sum(p['age'] for p in key_stats) / len(key_stats)
            avg_goals = sum(p['goals'] for p in key_stats) / len(key_stats)
            avg_assists = sum(p['assists'] for p in key_stats) / len(key_stats)
            
            # Age distribution
            age_groups = {
                'Young (18-23)': len([p for p in key_stats if 18 <= p['age'] <= 23]),
                'Prime (24-29)': len([p for p in key_stats if 24 <= p['age'] <= 29]),
                'Experienced (30+)': len([p for p in key_stats if p['age'] >= 30])
            }
            
            # Performance categories
            performance_categories = {
                'Elite (Rating > 15)': len([p for p in key_stats if p['performance_rating'] > 15]),
                'Excellent (10-15)': len([p for p in key_stats if 10 <= p['performance_rating'] <= 15]),
                'Good (5-10)': len([p for p in key_stats if 5 <= p['performance_rating'] < 10]),
                'Average (<5)': len([p for p in key_stats if p['performance_rating'] < 5])
            }
            
            # Top performers by category
            top_performers = {
                'goals': sorted(key_stats, key=lambda x: x['goals'], reverse=True)[:5],
                'assists': sorted(key_stats, key=lambda x: x['assists'], reverse=True)[:5],
                'performance': sorted(key_stats, key=lambda x: x['performance_rating'], reverse=True)[:5],
                'value': sorted(key_stats, key=lambda x: x['estimated_value'], reverse=True)[:5],
                'fitness': sorted(key_stats, key=lambda x: x['fitness_score'], reverse=True)[:5]
            }
            
            context = {
                'page_obj': page_obj,
                'players': page_obj.object_list,
                'total_players': total_players,
                'filtered_count': len(filtered_players),
                'positions': positions,
                'teams': teams,
                'current_filters': {
                    'position': position_filter,
                    'team': team_filter,
                    'sort': sort_by
                },
                'avg_age': avg_age,
                'avg_goals': avg_goals,
                'avg_assists': avg_assists,
                'age_groups': age_groups,
                'performance_categories': performance_categories,
                'top_performers': top_performers,
                'page_title': 'Players Analysis'
            }
            print(f"Enhanced players context: {len(filtered_players)} players, page {page_obj.number}")
    except Exception as e:
        print(f"Error in enhanced players: {e}")
        context = {'error': f'Error: {str(e)}'}
    
    return render(request, 'dashboard/players_enhanced.html', context)

def tactics_analysis(request):
    """Comprehensive tactics analysis page"""
    try:
        print("Loading tactics analysis page...")
        data = load_data()
        if data is None:
            context = {'error': 'Failed to load data'}
        else:
            key_stats = data.get('key_stats', [])
            matches_data = generate_match_data()
            
            # Tactical formations analysis (simulated)
            formations = {
                '4-3-3': {'usage': 35, 'avg_goals': 2.1, 'win_rate': 58},
                '4-2-3-1': {'usage': 28, 'avg_goals': 1.8, 'win_rate': 52},
                '3-5-2': {'usage': 15, 'avg_goals': 2.3, 'win_rate': 61},
                '4-4-2': {'usage': 12, 'avg_goals': 1.9, 'win_rate': 49},
                '5-3-2': {'usage': 10, 'avg_goals': 1.6, 'win_rate': 45}
            }
            
            # Playing styles analysis
            playing_styles = {
                'Possession-based': {
                    'teams': 12,
                    'avg_possession': 62.5,
                    'pass_accuracy': 87.2,
                    'goals_per_match': 1.9
                },
                'Counter-attacking': {
                    'teams': 8,
                    'avg_possession': 42.3,
                    'pass_accuracy': 78.5,
                    'goals_per_match': 2.1
                },
                'High-pressing': {
                    'teams': 7,
                    'avg_possession': 55.8,
                    'pass_accuracy': 82.1,
                    'goals_per_match': 2.3
                },
                'Defensive': {
                    'teams': 5,
                    'avg_possession': 38.9,
                    'pass_accuracy': 75.2,
                    'goals_per_match': 1.4
                }
            }
            
            # Position-based tactical analysis
            position_tactics = {}
            for player in key_stats:
                pos = player.get('position', 'Unknown')
                if pos not in position_tactics:
                    position_tactics[pos] = {
                        'players': 0,
                        'avg_pass_accuracy': 0,
                        'avg_dribbles': 0,
                        'avg_tackles': 0,
                        'avg_interceptions': 0,
                        'total_distance': 0
                    }
                
                position_tactics[pos]['players'] += 1
                position_tactics[pos]['avg_pass_accuracy'] += player['pass_accuracy']
                position_tactics[pos]['avg_dribbles'] += player['dribbles_successful']
                position_tactics[pos]['avg_tackles'] += player['tackles_won']
                position_tactics[pos]['avg_interceptions'] += player['interceptions']
                position_tactics[pos]['total_distance'] += player['distance_covered']
            
            # Calculate averages
            for pos_data in position_tactics.values():
                if pos_data['players'] > 0:
                    pos_data['avg_pass_accuracy'] /= pos_data['players']
                    pos_data['avg_dribbles'] /= pos_data['players']
                    pos_data['avg_tackles'] /= pos_data['players']
                    pos_data['avg_interceptions'] /= pos_data['players']
                    pos_data['avg_distance'] = pos_data['total_distance'] / pos_data['players']
            
            # Team tactical profiles (simulated)
            team_tactics = []
            teams = list(set(p.get('club', '') for p in key_stats if p.get('club')))[:16]
            
            for team in teams:
                team_players = [p for p in key_stats if p.get('club') == team]
                if team_players:
                    profile = {
                        'team': team,
                        'formation': random.choice(list(formations.keys())),
                        'style': random.choice(list(playing_styles.keys())),
                        'avg_possession': random.randint(35, 65),
                        'avg_pass_accuracy': sum(p['pass_accuracy'] for p in team_players) / len(team_players),
                        'pressing_intensity': random.choice(['Low', 'Medium', 'High', 'Very High']),
                        'defensive_line': random.choice(['Low', 'Medium', 'High']),
                        'attacking_width': random.choice(['Narrow', 'Balanced', 'Wide']),
                        'tempo': random.choice(['Slow', 'Medium', 'Fast', 'Very Fast'])
                    }
                    team_tactics.append(profile)
            
            # Tactical insights
            tactical_insights = [
                {
                    'title': 'Formation Effectiveness',
                    'description': '3-5-2 formation shows highest win rate at 61%',
                    'icon': 'fas fa-chess-board',
                    'color': 'success'
                },
                {
                    'title': 'High-Pressing Success',
                    'description': 'Teams using high-pressing average 2.3 goals per match',
                    'icon': 'fas fa-running',
                    'color': 'info'
                },
                {
                    'title': 'Possession vs Results',
                    'description': 'Counter-attacking teams more clinical despite less possession',
                    'icon': 'fas fa-chart-line',
                    'color': 'warning'
                }
            ]
            
            context = {
                'formations': formations,
                'playing_styles': playing_styles,
                'position_tactics': position_tactics,
                'team_tactics': team_tactics,
                'tactical_insights': tactical_insights,
                'page_title': 'Tactical Analysis'
            }
            print(f"Tactics context: {len(formations)} formations, {len(playing_styles)} styles")
    except Exception as e:
        print(f"Error in tactics_analysis: {e}")
        context = {'error': f'Error: {str(e)}'}
    
    return render(request, 'dashboard/tactics.html', context)
