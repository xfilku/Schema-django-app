"""
Admin configuration for custom models and extended User model integration.

This module registers Tag, UserPermissions, and UserLogSettings models
to the Django admin interface and customizes the default User admin panel
to include inline logging preferences.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Tag, UserLogSettings, UserPermissions
from .forms import TagAdminForm


# --- Tag admin ---
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin configuration for Tag model.
    """
    form = TagAdminForm  # Custom form with additional validation/styling
    list_display = ('name', 'color')  # Displayed columns in admin list view
    search_fields = ('name',)  # Enables search by name


@admin.register(UserPermissions)
class UserPermissionsAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserPermissions model.
    """
    list_display = ['user']
    readonly_fields = ['user']  # Prevent editing user field
    search_fields = ['user__username']  # Allow search by username


# --- UserLogSettings inline for User admin ---
class UserLogSettingsInline(admin.StackedInline):
    """
    Inline admin class to display and edit UserLogSettings
    directly within the User admin panel.
    """
    model = UserLogSettings
    can_delete = False  # Prevent deletion via inline
    verbose_name_plural = 'Ustawienia logowania'  # Displayed name in admin


# --- Extended UserAdmin with inlines ---
class UserAdmin(BaseUserAdmin):
    """
    Custom User admin including UserLogSettings inline.
    """
    inlines = (UserLogSettingsInline,)  # Attach inline settings to User view


# --- Override default User admin ---
admin.site.unregister(User)  # Unregister built-in User admin
admin.site.register(User, UserAdmin)  # Register custom User admin
