"""
URL configuration for the 'solution' Django project.

This file defines the root URL mappings used by the Django application.
Routes are defined using `urlpatterns` and point to URL configurations
in individual apps or views.

Docs: https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Route to the Django admin panel
    path('admin/', admin.site.urls),

    # Main app routes delegated to 'web_service' application
    path('', include('web_service.urls')),
]

# Custom 404 error handler (defined in web_service/views.py)
handler404 = 'web_service.views.custom_404_view'
