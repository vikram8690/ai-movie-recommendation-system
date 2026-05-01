"""
reviews/views.py
Add a review (with AI sentiment), view review history, and export to CSV.
"""

import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from movies.models import Movie
from .models import Review
from .forms import ReviewForm
from utils.sentiment_utils import predict_sentiment


# ------------------------------------------------------------------ #
#  Add / edit review                                                  #
# ------------------------------------------------------------------ #
@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    # If user already reviewed this movie, let them edit it
    existing = Review.objects.filter(user=request.user, movie=movie).first()

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing)
        if form.is_valid():
            review          = form.save(commit=False)
            review.user     = request.user
            review.movie    = movie
            # ---- AI Sentiment Analysis ----
            review.sentiment = predict_sentiment(review.review_text)
            review.save()

            action = 'updated' if existing else 'submitted'
            messages.success(
                request,
                f'Review {action}! Sentiment detected: '
                f'<strong>{review.sentiment.capitalize()}</strong>'
            )
            return redirect('movie_detail', pk=movie_id)
        else:
            messages.error(request, 'Please fix the form errors.')
    else:
        form = ReviewForm(instance=existing)

    context = {
        'form':     form,
        'movie':    movie,
        'existing': existing,
    }
    return render(request, 'reviews/add_review.html', context)


# ------------------------------------------------------------------ #
#  Review history                                                     #
# ------------------------------------------------------------------ #
@login_required
def review_history(request):
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'reviews/review_history.html', {'reviews': reviews})


# ------------------------------------------------------------------ #
#  Export reviews as CSV                                              #
# ------------------------------------------------------------------ #
@login_required
def export_reviews_csv(request):
    """Download all of the logged-in user's reviews as a CSV file."""
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="my_reviews.csv"'

    writer = csv.writer(response)
    writer.writerow(['Movie', 'Rating', 'Sentiment', 'Review Text', 'Date'])

    for r in reviews:
        writer.writerow([
            r.movie.title,
            r.rating,
            r.sentiment,
            r.review_text,
            r.created_at.strftime('%Y-%m-%d %H:%M'),
        ])

    return response
