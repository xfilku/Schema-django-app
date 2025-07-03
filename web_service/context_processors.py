"""
Custom context processors for global template variables.

These functions inject user-specific data (favorites, settings, permissions)
into the template context, available in all templates.
"""

from .models import FavoriteLink, UserSilentSettings
from django.conf import settings

def user_favorites(request):
    """
    Add the current user's favorite links to the template context.

    Returns:
        dict: A dictionary with user's favorite links, their URLs and names.
    """
    if request.user.is_authenticated:
        favorites = FavoriteLink.objects.filter(user=request.user)
        return {
            'user_favorites': favorites,
            'favorite_url_names': [fav.url for fav in favorites],
            'favorite_names': [fav.name for fav in favorites],
        }
    return {
        'user_favorites': [],
        'favorite_url_names': [],
        'favorite_names': [],
    }


def per_page_setting(request):
    """
    Add the user's per-page setting (pagination size) to the context.

    Returns:
        dict: {'global_per_page': int}
    """
    if request.user.is_authenticated:
        setting = UserSilentSettings.objects.filter(user=request.user).first()
        return {'global_per_page': setting.per_page if setting else 20}
    return {'global_per_page': 20}


def user_permissions(request):
    """
    Add custom user permissions to the template context.

    Returns:
        dict: {'USER_PERMS': dict} if available, empty dict otherwise.
    """
    if not request.user.is_authenticated:
        return {}

    # Use attached custom permission object if present
    perms = getattr(request.user, 'custom_permissions', None)
    return {
        'USER_PERMS': perms.permissions if perms else {}
    }

"""
Custom context processors to inject global variables into all templates.
"""

def global_variables(request):
    """
    Adds global application constants to the template context.

    Returns:
        dict: A dictionary with APP_NAME and APP_OWNER from settings.
    """
    return {
        'APP_NAME': getattr(settings, 'APP_NAME', 'AppName'),
        'APP_OWNER': getattr(settings, 'APP_OWNER', 'Owner'),
    }

