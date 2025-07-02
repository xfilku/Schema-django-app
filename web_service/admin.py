from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Tag, UserLogSettings, UserPermissions
from .forms import TagAdminForm


# --- Tag admin ---
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    form = TagAdminForm
    list_display = ('name', 'color',)
    search_fields = ('name',)

@admin.register(UserPermissions)
class UserPermissionsAdmin(admin.ModelAdmin):
    list_display = ['user']
    readonly_fields = ['user']
    search_fields = ['user__username']

# --- UserLogSettings inline dla użytkownika ---
class UserLogSettingsInline(admin.StackedInline):
    model = UserLogSettings
    can_delete = False
    verbose_name_plural = 'Ustawienia logowania'


# --- Rozszerzony UserAdmin ---
class UserAdmin(BaseUserAdmin):
    inlines = (UserLogSettingsInline,)


# --- Przerejestrowanie użytkownika ---
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
