"""
Utilities for handling custom user permissions.

Includes decorators and helper functions to check whether a user
has specific module-level access rights stored in UserPermissions.
"""

from functools import wraps
from django.shortcuts import redirect, render
from django.urls import reverse


def user_has_permission(user, code):
    """
    Check if the given user has the specified permission code.

    Admin and staff users are granted all permissions automatically.

    Args:
        user (User): Django user instance.
        code (str): Permission code to check.

    Returns:
        bool: True if user has permission, False otherwise.
    """
    #superusers and staff_members have full access
    if user.is_superuser or user.is_staff:
        return True
    if not user.is_authenticated:
        return False
    if not hasattr(user, 'custom_permissions'):
        return False
    return user.custom_permissions.permissions.get(code, False)


def permission_required(code):
    """
    Decorator for view functions that require a specific permission.

    If the user is not authenticated, redirects to login.
    If the user lacks the required permission, renders a 403 error page.

    Args:
        code (str): Permission code to check (e.g. 'announcement.view').

    Returns:
        function: Wrapped view function.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(f"{reverse('login')}?next={request.path}")

            if not user_has_permission(request.user, code):
                return render(request, 'errors/403.html')  # 🛑 Brak uprawnień

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
