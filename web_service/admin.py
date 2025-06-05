from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Tag, UserLogSettings, PhoneContact
from .forms import TagAdminForm


# --- Tag admin ---
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    form = TagAdminForm
    list_display = ('name', 'color',)
    search_fields = ('name',)


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

@admin.register(PhoneContact)
class PhoneContactAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'phone_number', 'city', 'status', 'contact_date', 'user')
    list_filter = ('status', 'tag', 'city')
    search_fields = ('company_name', 'nip', 'phone_number', 'city')
    ordering = ('-contact_date',)

