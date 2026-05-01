"""
movies/views.py
Movie listing, detail, CRUD (admin only), and trending page.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg

from .models import Movie, GENRE_CHOICES
from .forms import MovieForm
from reviews.models import Review
from recommendations.models import Watchlist


# ------------------------------------------------------------------ #
#  Helper: check if a user has admin role                             #
# ------------------------------------------------------------------ #
def _is_admin(user):
    if user.is_superuser:
        return True
    try:
        return user.userprofile.role == 'admin'
    except Exception:
        return False


# ------------------------------------------------------------------ #
#  Movie list with search / filter / pagination                       #
# ------------------------------------------------------------------ #
def movie_list(request):
    movies = Movie.objects.annotate(avg_rating=Avg('review__rating'), review_count=Count('review'))

    # --- search ---
    query = request.GET.get('q', '').strip()
    if query:
        movies = movies.filter(
            Q(title__icontains=query)    |
            Q(genre__icontains=query)    |
            Q(director__icontains=query) |
            Q(actors__icontains=query)
        )

    # --- genre filter ---
    genre = request.GET.get('genre', '')
    if genre:
        movies = movies.filter(genre=genre)

    # --- year filter ---
    year = request.GET.get('year', '')
    if year:
        movies = movies.filter(release_year=year)

    # --- minimum rating filter ---
    min_rating = request.GET.get('min_rating', '')
    if min_rating:
        try:
            movies = movies.filter(avg_rating__gte=float(min_rating))
        except ValueError:
            pass

    # --- sort ---
    sort = request.GET.get('sort', '-created_at')
    allowed_sorts = ['-created_at', 'created_at', 'title', '-avg_rating', '-review_count']
    if sort in allowed_sorts:
        movies = movies.order_by(sort)
    else:
        movies = movies.order_by('-created_at')

    # --- pagination (12 per page) ---
    paginator  = Paginator(movies, 12)
    page_obj   = paginator.get_page(request.GET.get('page', 1))

    # Year dropdown — from current year down to 1980
    years = range(2024, 1979, -1)

    context = {
        'page_obj':       page_obj,
        'query':          query,
        'genres':         GENRE_CHOICES,
        'years':          years,
        'selected_genre': genre,
        'selected_year':  year,
        'selected_rating': min_rating,
        'selected_sort':  sort,
    }
    return render(request, 'movies/movie_list.html', context)


# ------------------------------------------------------------------ #
#  Movie detail                                                       #
# ------------------------------------------------------------------ #
def movie_detail(request, pk):
    movie       = get_object_or_404(Movie, pk=pk)
    reviews     = Review.objects.filter(movie=movie).order_by('-created_at')
    avg_rating  = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    avg_rating  = round(avg_rating, 1)

    user_review  = None
    in_watchlist = False

    if request.user.is_authenticated:
        user_review  = Review.objects.filter(user=request.user, movie=movie).first()
        in_watchlist = Watchlist.objects.filter(user=request.user, movie=movie).exists()

    similar = Movie.objects.filter(genre=movie.genre).exclude(pk=pk).order_by('?')[:4]

    # Sentiment counts for this movie
    pos = reviews.filter(sentiment='positive').count()
    neg = reviews.filter(sentiment='negative').count()
    neu = reviews.filter(sentiment='neutral').count()

    context = {
        'movie':        movie,
        'reviews':      reviews,
        'avg_rating':   avg_rating,
        'star_range':   range(1, 6),
        'user_review':  user_review,
        'in_watchlist': in_watchlist,
        'similar':      similar,
        'pos':          pos,
        'neg':          neg,
        'neu':          neu,
    }
    return render(request, 'movies/movie_detail.html', context)


# ------------------------------------------------------------------ #
#  Add movie (admin only)                                             #
# ------------------------------------------------------------------ #
@login_required
def movie_add(request):
    if not _is_admin(request.user):
        messages.error(request, 'Access denied. Admins only.')
        return redirect('movie_list')

    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save()
            messages.success(request, f'"{movie.title}" added successfully!')
            return redirect('movie_detail', pk=movie.pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = MovieForm()

    return render(request, 'movies/movie_add.html', {'form': form})


# ------------------------------------------------------------------ #
#  Edit movie (admin only)                                            #
# ------------------------------------------------------------------ #
@login_required
def movie_edit(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if not _is_admin(request.user):
        messages.error(request, 'Access denied. Admins only.')
        return redirect('movie_list')

    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{movie.title}" updated successfully!')
            return redirect('movie_detail', pk=pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = MovieForm(instance=movie)

    return render(request, 'movies/movie_edit.html', {'form': form, 'movie': movie})


# ------------------------------------------------------------------ #
#  Delete movie (admin only)                                          #
# ------------------------------------------------------------------ #
@login_required
def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if not _is_admin(request.user):
        messages.error(request, 'Access denied. Admins only.')
        return redirect('movie_list')

    if request.method == 'POST':
        title = movie.title
        movie.delete()
        messages.success(request, f'"{title}" deleted successfully!')
        return redirect('movie_list')

    return render(request, 'movies/movie_delete_confirm.html', {'movie': movie})


# ------------------------------------------------------------------ #
#  Trending movies                                                    #
# ------------------------------------------------------------------ #
def trending_movies(request):
    """Movies ordered by number of reviews (most-reviewed = most trending)."""
    movies = (
        Movie.objects
        .annotate(review_count=Count('review'), avg_rating=Avg('review__rating'))
        .order_by('-review_count')[:20]
    )
    return render(request, 'movies/trending.html', {'movies': movies})
