"""
reviews/models.py
Review model — stores user ratings, text reviews, and AI sentiment.
"""

from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie
from django.core.validators import MinValueValidator, MaxValueValidator


SENTIMENT_CHOICES = [
    ('positive', 'Positive'),
    ('negative', 'Negative'),
    ('neutral',  'Neutral'),
]


class Review(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    movie       = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating      = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Rating from 1 (worst) to 5 (best)'
    )
    review_text = models.TextField(help_text='Write your thoughts about the movie')
    sentiment   = models.CharField(max_length=10, choices=SENTIMENT_CHOICES, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')   # one review per user per movie
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} → {self.movie.title} ({self.rating}★)"

    def sentiment_badge_class(self):
        """Returns Bootstrap badge colour class for the sentiment."""
        return {
            'positive': 'success',
            'negative': 'danger',
            'neutral':  'warning',
        }.get(self.sentiment, 'secondary')
