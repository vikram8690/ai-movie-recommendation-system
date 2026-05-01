"""reviews/admin.py"""

from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display   = ('user', 'movie', 'rating', 'sentiment', 'created_at')
    list_filter    = ('sentiment', 'rating', 'created_at')
    search_fields  = ('user__username', 'movie__title', 'review_text')
    readonly_fields = ('sentiment', 'created_at')
    ordering       = ('-created_at',)
