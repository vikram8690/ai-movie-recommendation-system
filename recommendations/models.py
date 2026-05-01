"""
recommendations/models.py
Watchlist and RecommendationLog models.
"""

from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie


class Watchlist(models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    movie    = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} → {self.movie.title}"


class RecommendationLog(models.Model):
    """Stores each recommendation event so we can track what was recommended."""
    user              = models.ForeignKey(User, on_delete=models.CASCADE)
    recommended_movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    score             = models.FloatField(default=0.0)
    created_at        = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} ← {self.recommended_movie.title} ({self.score:.2f})"
