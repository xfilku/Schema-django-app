"""
URL configuration for the 'web_service' Django application.

Defines routing for views related to account management, tags, logs,
announcements, user administration, and info service settings.
"""

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView, LoginView

from .views import (
    main_page,
    account_settings,
    change_password,
    tag_list,
    tag_create,
    tag_edit,
    tag_delete,
    log_list,
    toggle_favorite,
    info_service_configuration,
    announcement_list,
    announcement_create,
    announcement_edit,
    announcement_delete,
    user_list,
    user_create,
    user_edit,
    user_delete,
)

urlpatterns = [
    # Dashboard
    path('', main_page, name='main_page'),

    # Authentication
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Account
    path('account/settings/', account_settings, name='account_settings'),
    path('change-password/', change_password, name='change_password'),

    # Tags (Flagi)
    path('tags/', tag_list, name='tag_list'),
    path('tags/create/', tag_create, name='tag_create'),
    path('tags/<int:pk>/edit/', tag_edit, name='tag_edit'),
    path('tags/<int:pk>/delete/', tag_delete, name='tag_delete'),

    # Logs (Dziennik aktywności)
    path('logs/', log_list, name='log_list'),

    # Favorites (Ulubione linki)
    path('toggle-favorite/', toggle_favorite, name='toggle_favorite'),

    # Info service configuration
    path('info_service_configuration', info_service_configuration, name='info_service_configuration'),

    # Announcements
    path('announcementlist/', announcement_list, name='announcement_list'),
    path('announcement/create/', announcement_create, name='announcement_create'),
    path('announcement/<int:pk>/edit/', announcement_edit, name='announcement_edit'),
    path('announcement/<int:pk>/delete/', announcement_delete, name='announcement_delete'),

    # User management
    path('users/', user_list, name='user_list'),
    path('users/create/', user_create, name='user_create'),
    path('users/<int:pk>/edit/', user_edit, name='user_edit'),
    path('users/<int:pk>/delete/', user_delete, name='user_delete'),
]

# Static/media files in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
