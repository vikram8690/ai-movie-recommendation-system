"""dashboard/urls.py"""

from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
]
