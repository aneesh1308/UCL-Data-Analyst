from django.db import models

# Create your models here.

class Player(models.Model):
    """Player model to store key statistics"""
    player_name = models.CharField(max_length=100)
    club = models.CharField(max_length=50)
    position = models.CharField(max_length=20)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    minutes_played = models.IntegerField(default=0)
    match_played = models.IntegerField(default=0)
    distance_covered = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"{self.player_name} ({self.club})"
    
    @property
    def goals_per_match(self):
        return self.goals / self.match_played if self.match_played > 0 else 0
    
    @property
    def goal_contribution(self):
        return self.goals + self.assists
    
    @property
    def goals_per_90(self):
        return (self.goals / self.minutes_played * 90) if self.minutes_played > 0 else 0

class GoalStats(models.Model):
    """Goal statistics for players"""
    player_name = models.CharField(max_length=100)
    club = models.CharField(max_length=50)
    goals = models.IntegerField(default=0)
    right_foot = models.IntegerField(default=0)
    left_foot = models.IntegerField(default=0)
    headers = models.IntegerField(default=0)
    penalties = models.IntegerField(default=0)
    inside_area = models.IntegerField(default=0)
    outside_areas = models.IntegerField(default=0)
    match_played = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.player_name} - {self.goals} goals"

class AttackingStats(models.Model):
    """Attacking statistics for players"""
    player_name = models.CharField(max_length=100)
    club = models.CharField(max_length=50)
    assists = models.IntegerField(default=0)
    corners_taken = models.IntegerField(default=0)
    offsides = models.IntegerField(default=0)
    dribbles = models.IntegerField(default=0)
    match_played = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.player_name} - {self.assists} assists"

class DefendingStats(models.Model):
    """Defending statistics for players"""
    player_name = models.CharField(max_length=100)
    club = models.CharField(max_length=50)
    balls_recovered = models.IntegerField(default=0)
    tackles = models.IntegerField(default=0)
    tackles_won = models.IntegerField(default=0)
    clearance_attempted = models.IntegerField(default=0)
    match_played = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.player_name} - {self.tackles} tackles"

class GoalkeepingStats(models.Model):
    """Goalkeeper statistics"""
    player_name = models.CharField(max_length=100)
    club = models.CharField(max_length=50)
    saves = models.IntegerField(default=0)
    goals_conceded = models.IntegerField(default=0)
    saves_from_penalty = models.IntegerField(default=0)
    punches = models.IntegerField(default=0)
    match_played = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.player_name} - {self.saves} saves"
    
    @property
    def save_percentage(self):
        total_shots = self.saves + self.goals_conceded
        return (self.saves / total_shots * 100) if total_shots > 0 else 0

class DisciplinaryStats(models.Model):
    """Disciplinary statistics"""
    player_name = models.CharField(max_length=100)
    club = models.CharField(max_length=50)
    fouls = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)
    match_played = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.player_name} - {self.yellow_cards}Y, {self.red_cards}R"
