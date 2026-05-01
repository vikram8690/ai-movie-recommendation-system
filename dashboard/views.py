"""
dashboard/views.py
Admin-only dashboard showing system-wide statistics.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Avg

from movies.models import Movie
from reviews.models import Review
from recommendations.models import Watchlist, RecommendationLog
from accounts.models import UserProfile


def _is_admin(user):
    if user.is_superuser:
        return True
    try:
        return user.userprofile.role == 'admin'
    except Exception:
        return False


@login_required
def admin_dashboard(request):
    if not _is_admin(request.user):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')

    # --- Site-wide stats ---
    total_users   = User.objects.count()
    total_movies  = Movie.objects.count()
    total_reviews = Review.objects.count()
    total_wl      = Watchlist.objects.count()

    # --- Sentiment breakdown ---
    pos = Review.objects.filter(sentiment='positive').count()
    neg = Review.objects.filter(sentiment='negative').count()
    neu = Review.objects.filter(sentiment='neutral').count()

    # --- Top rated movies ---
    top_movies = (
        Movie.objects
        .annotate(avg_rating=Avg('review__rating'), rc=Count('review'))
        .filter(rc__gt=0)
        .order_by('-avg_rating')[:5]
    )

    # --- Recent reviews ---
    recent_reviews = Review.objects.order_by('-created_at')[:10]

    # --- Most active users ---
    top_users = (
        User.objects
        .annotate(rc=Count('review'))
        .order_by('-rc')[:5]
    )

    # --- Genre distribution ---
    genre_data = (
        Movie.objects
        .values('genre')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    context = {
        'total_users':    total_users,
        'total_movies':   total_movies,
        'total_reviews':  total_reviews,
        'total_wl':       total_wl,
        'pos':            pos,
        'neg':            neg,
        'neu':            neu,
        'top_movies':     top_movies,
        'recent_reviews': recent_reviews,
        'top_users':      top_users,
        'genre_data':     genre_data,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)
