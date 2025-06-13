from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('test/', views.test_view, name='test'),
    path('test-data/', views.test_data_view, name='test_data'),
    path('', views.overview, name='overview'),
    path('players/', views.players, name='players'),
    path('teams/', views.teams, name='teams'),
    path('goals/', views.goals_and_scoring, name='goals'),
    path('matches/', views.matches, name='matches'),
    path('tactics/', views.tactics_analysis, name='tactics'),
    path('advanced-analytics/', views.advanced_analytics, name='advanced_analytics'),
    path('tactical-analysis/', views.tactical_analysis, name='tactical_analysis'),
    path('comprehensive-dashboard/', views.comprehensive_dashboard, name='comprehensive_dashboard'),
    
    # Additional URL patterns referenced in templates
    path('statistics/', views.overview, name='statistics'),  # Redirect to overview for now
    path('insights/', views.advanced_analytics, name='insights'),  # Redirect to advanced_analytics
    path('performance/', views.players, name='performance'),  # Redirect to players for now
    
    # API Endpoints
    path('api/player/<str:player_name>/', views.get_player_data, name='player_api'),
    path('api/team/<str:team_name>/', views.get_team_data, name='team_api'),
] 