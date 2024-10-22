"""Defines URL patterns for accounts."""
from django.urls import path, include
from .views import CustomLoginView
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),  # Use the custom login view
    # Include default auth urls.
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
]