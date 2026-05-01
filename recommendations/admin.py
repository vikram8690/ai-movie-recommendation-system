"""recommendations/admin.py"""

from django.contrib import admin
from .models import Watchlist, RecommendationLog


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display  = ('user', 'movie', 'added_at')
    list_filter   = ('added_at',)
    search_fields = ('user__username', 'movie__title')


@admin.register(RecommendationLog)
class RecommendationLogAdmin(admin.ModelAdmin):
    list_display  = ('user', 'recommended_movie', 'score', 'created_at')
    list_filter   = ('created_at',)
    search_fields = ('user__username', 'recommended_movie__title')
    readonly_fields = ('created_at',)
