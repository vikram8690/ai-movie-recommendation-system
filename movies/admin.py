"""movies/admin.py"""

from django.contrib import admin
from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display   = ('title', 'genre', 'release_year', 'director', 'created_at')
    list_filter    = ('genre', 'release_year')
    search_fields  = ('title', 'director', 'actors')
    ordering       = ('-created_at',)
    readonly_fields = ('created_at',)
