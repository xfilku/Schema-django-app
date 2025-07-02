from functools import wraps
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponseForbidden

def user_has_permission(user, code):
    # ✅ Jeśli admin lub staff – ma wszystko
    if user.is_superuser or user.is_staff:
        return True
    if not user.is_authenticated:
        return False
    if not hasattr(user, 'custom_permissions'):
        return False
    return user.custom_permissions.permissions.get(code, False)

def permission_required(code):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(f"{reverse('login')}?next={request.path}")
            if not user_has_permission(request.user, code):
                return render(request, 'errors/403.html')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator