from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
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
