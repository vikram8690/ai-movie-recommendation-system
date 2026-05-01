"""Main URL configuration for AI Movie System."""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Accounts (home, register, login, logout, dashboard)
    path('', include('accounts.urls')),

    # Movies (list, detail, add, edit, delete, trending)
    path('movies/', include('movies.urls')),

    # Reviews (add, history, export)
    path('reviews/', include('reviews.urls')),

    # Recommendations & Watchlist
    path('recommendations/', include('recommendations.urls')),

    # Admin dashboard
    path('dashboard/', include('dashboard.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
