"""reviews/urls.py"""

from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:movie_id>/', views.add_review,         name='add_review'),
    path('history/',            views.review_history,     name='review_history'),
    path('export/',             views.export_reviews_csv, name='export_reviews_csv'),
]
