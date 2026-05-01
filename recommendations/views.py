"""
recommendations/views.py
Personalised recommendation page and watchlist management.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from movies.models import Movie
from .models import Watchlist, RecommendationLog
from utils.recommendation_utils import get_recommendations


# ------------------------------------------------------------------ #
#  Recommendations page                                               #
# ------------------------------------------------------------------ #
@login_required
def recommendations(request):
    """Show AI-generated personalised recommendations for the logged-in user."""
    recommended = get_recommendations(request.user, top_n=10)

    # Also fetch the last 5 logged recommendations for display
    logs = RecommendationLog.objects.filter(user=request.user).order_by('-created_at')[:5]

    context = {
        'recommended': recommended,
        'logs':        logs,
    }
    return render(request, 'recommendations/recommendations.html', context)


# ------------------------------------------------------------------ #
#  Watchlist                                                          #
# ------------------------------------------------------------------ #
@login_required
def watchlist(request):
    items = Watchlist.objects.filter(user=request.user).select_related('movie')
    return render(request, 'recommendations/watchlist.html', {'items': items})


@login_required
def add_to_watchlist(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    _, created = Watchlist.objects.get_or_create(user=request.user, movie=movie)
    if created:
        messages.success(request, f'"{movie.title}" added to your watchlist.')
    else:
        messages.info(request, f'"{movie.title}" is already in your watchlist.')
    return redirect(request.META.get('HTTP_REFERER', 'watchlist'))


@login_required
def remove_from_watchlist(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    deleted, _ = Watchlist.objects.filter(user=request.user, movie=movie).delete()
    if deleted:
        messages.success(request, f'"{movie.title}" removed from your watchlist.')
    return redirect(request.META.get('HTTP_REFERER', 'watchlist'))
