"""
accounts/views.py
Handles user registration, login, logout, and the user dashboard.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Count, Avg

from .forms import RegistrationForm
from .models import UserProfile
from movies.models import Movie
from reviews.models import Review
from recommendations.models import Watchlist
from utils.recommendation_utils import get_recommendations


# ------------------------------------------------------------------ #
#  Home page                                                          #
# ------------------------------------------------------------------ #
def home(request):
    """Public landing page — shows trending movies to anonymous visitors."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    # Top-6 movies by review count
    trending = (
        Movie.objects
        .annotate(review_count=Count('review'))
        .order_by('-review_count')[:6]
    )
    return render(request, 'home.html', {'trending': trending})


# ------------------------------------------------------------------ #
#  Register                                                           #
# ------------------------------------------------------------------ #
def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


# ------------------------------------------------------------------ #
#  Login                                                              #
# ------------------------------------------------------------------ #
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            # Redirect to ?next= URL if present
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


# ------------------------------------------------------------------ #
#  Logout                                                             #
# ------------------------------------------------------------------ #
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


# ------------------------------------------------------------------ #
#  User Dashboard                                                     #
# ------------------------------------------------------------------ #
@login_required
def dashboard(request):
    """
    Personalised dashboard showing stats, recent reviews,
    watchlist items and personalised recommendations.
    """
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    review_count    = Review.objects.filter(user=request.user).count()
    watchlist_count = Watchlist.objects.filter(user=request.user).count()
    recent_reviews  = Review.objects.filter(user=request.user).order_by('-created_at')[:5]
    recommendations = get_recommendations(request.user, top_n=4)
    total_movies    = Movie.objects.count()

    # Sentiment breakdown for current user
    pos = Review.objects.filter(user=request.user, sentiment='positive').count()
    neg = Review.objects.filter(user=request.user, sentiment='negative').count()
    neu = Review.objects.filter(user=request.user, sentiment='neutral').count()

    context = {
        'profile':          profile,
        'review_count':     review_count,
        'watchlist_count':  watchlist_count,
        'recent_reviews':   recent_reviews,
        'recommendations':  recommendations,
        'total_movies':     total_movies,
        'pos_count':        pos,
        'neg_count':        neg,
        'neu_count':        neu,
    }
    return render(request, 'accounts/dashboard.html', context)
