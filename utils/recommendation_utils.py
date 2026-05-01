"""
utils/recommendation_utils.py

Content-based movie recommendation engine.
Combines movie title, genre, description, actors, and director into a
TF-IDF feature vector, then uses cosine similarity to find movies that
are most similar to movies the user has rated highly (4-5 stars).

No pre-training required — similarity is computed on-the-fly using the
current database content.
"""

import numpy as np


def _build_feature_string(movie) -> str:
    """
    Concatenate all text attributes of a movie into one string for TF-IDF.
    Repeat genre and director so they carry more weight in the similarity.
    """
    parts = [
        movie.title,
        movie.genre,     # repeated for extra weight
        movie.genre,
        movie.description,
        movie.actors,
        movie.director,  # repeated for extra weight
        movie.director,
    ]
    return ' '.join(str(p) for p in parts).lower()


def get_recommendations(user, top_n: int = 5):
    """
    Return a list of up to `top_n` Movie objects recommended for `user`.

    Algorithm:
    1. Collect movies the user has already reviewed or watchlisted → exclude these.
    2. Get the user's highly rated movies (rating >= 4) as "seed" movies.
    3. Build a TF-IDF matrix for all movies.
    4. For each seed movie compute cosine similarity against all other movies.
    5. Aggregate scores (max weighted by the user's rating).
    6. Return top-N movies sorted by score.
    7. If the user has no high-rated movies, fall back to most-reviewed movies.
    """
    # Import here to avoid circular imports at module load time
    from movies.models import Movie
    from reviews.models import Review
    from recommendations.models import Watchlist, RecommendationLog

    all_movies = list(Movie.objects.all())
    if len(all_movies) < 2:
        return []

    # Movies to exclude (already reviewed or watchlisted)
    reviewed_ids    = set(Review.objects.filter(user=user).values_list('movie_id', flat=True))
    watchlisted_ids = set(Watchlist.objects.filter(user=user).values_list('movie_id', flat=True))
    excluded_ids    = reviewed_ids | watchlisted_ids

    # Seed movies: highly rated (≥4 stars)
    liked = list(Review.objects.filter(user=user, rating__gte=4).select_related('movie'))

    # Fallback: no liked movies → return newest movies not yet seen
    if not liked:
        fallback = Movie.objects.exclude(id__in=excluded_ids).order_by('-created_at')[:top_n]
        return list(fallback)

    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        # Build feature strings for every movie
        features = [_build_feature_string(m) for m in all_movies]

        tfidf        = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        tfidf_matrix = tfidf.fit_transform(features)

        # Map movie id → matrix row index
        idx_map = {m.id: i for i, m in enumerate(all_movies)}

        scores = {}
        for review in liked:
            seed_id  = review.movie_id
            seed_idx = idx_map.get(seed_id)
            if seed_idx is None:
                continue

            sim_row = cosine_similarity(tfidf_matrix[seed_idx], tfidf_matrix).flatten()

            for i, sim_score in enumerate(sim_row):
                movie = all_movies[i]
                if movie.id in excluded_ids or movie.id == seed_id:
                    continue
                weighted = float(sim_score) * review.rating   # weight by user rating
                scores[movie.id] = max(scores.get(movie.id, 0), weighted)

        # Sort by score descending
        sorted_ids = sorted(scores, key=lambda x: scores[x], reverse=True)[:top_n]

        recommended = []
        for mid in sorted_ids:
            try:
                movie = Movie.objects.get(id=mid)
                recommended.append(movie)
                # Log this recommendation
                RecommendationLog.objects.update_or_create(
                    user=user,
                    recommended_movie=movie,
                    defaults={'score': scores[mid]},
                )
            except Movie.DoesNotExist:
                pass

        # If we found fewer than top_n, pad with newest unseen movies
        if len(recommended) < top_n:
            seen_now = excluded_ids | {m.id for m in recommended}
            extra = list(
                Movie.objects.exclude(id__in=seen_now).order_by('-created_at')[:top_n - len(recommended)]
            )
            recommended.extend(extra)

        return recommended

    except Exception:
        # Any ML error → graceful fallback
        return list(Movie.objects.exclude(id__in=excluded_ids).order_by('-created_at')[:top_n])
