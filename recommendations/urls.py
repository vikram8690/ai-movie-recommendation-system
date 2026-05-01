"""recommendations/urls.py"""

from django.urls import path
from . import views

urlpatterns = [
    path('',                           views.recommendations,       name='recommendations'),
    path('watchlist/',                 views.watchlist,             name='watchlist'),
    path('watchlist/add/<int:movie_id>/',    views.add_to_watchlist,    name='add_to_watchlist'),
    path('watchlist/remove/<int:movie_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
]
