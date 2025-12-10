from django.db import models

# Create your models here.
class UserProfile(models.Model):
    ROLES = [
        ('administrator', 'Administrator'),
        ('utilizator', 'Utilizator'),
    ]
    
    keycloak_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLES, default='utilizator')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username

class Match(models.Model):
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    match_date = models.DateTimeField()
    
    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"