"""
movies/models.py
Core Movie model.
"""

from django.db import models
from django.db.models import Avg


GENRE_CHOICES = [
    ('action',       'Action'),
    ('adventure',    'Adventure'),
    ('animation',    'Animation'),
    ('biography',    'Biography'),
    ('comedy',       'Comedy'),
    ('crime',        'Crime'),
    ('documentary',  'Documentary'),
    ('drama',        'Drama'),
    ('fantasy',      'Fantasy'),
    ('horror',       'Horror'),
    ('mystery',      'Mystery'),
    ('romance',      'Romance'),
    ('sci-fi',       'Sci-Fi'),
    ('thriller',     'Thriller'),
    ('musical',      'Musical'),
]


class Movie(models.Model):
    title        = models.CharField(max_length=200)
    description  = models.TextField()
    genre        = models.CharField(max_length=50, choices=GENRE_CHOICES)
    release_year = models.IntegerField()
    director     = models.CharField(max_length=200)
    actors       = models.TextField(help_text='Comma-separated list of actors')
    poster       = models.ImageField(upload_to='posters/', null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.release_year})"

    def average_rating(self):
        """Returns average rating rounded to 1 decimal place, or 0 if no reviews."""
        result = self.review_set.aggregate(avg=Avg('rating'))['avg']
        return round(result, 1) if result else 0

    def review_count(self):
        return self.review_set.count()

    def get_poster_url(self):
        """Returns poster URL or a placeholder."""
        if self.poster and hasattr(self.poster, 'url'):
            return self.poster.url
        return f"https://placehold.co/300x450/1a1a2e/f5c518?text={self.title[:15].replace(' ', '+')}"
