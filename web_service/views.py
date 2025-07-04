"""
Views for web_service application.

Handles dashboard, account management, tag system, announcement module,
activity logging, user management, and favorites functionality.
"""

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.paginator import Paginator

from .forms import (
    UserSettingsForm, TagForm, InfoServiceConfigurationForm,
    AnnouncementForm, CustomUserCreateForm, CustomUserEditForm
)
from .models import (
    Tag, Log, FavoriteLink, UserSilentSettings,
    InfoServiceConfiguration, Announcement
)
from .permissions_utils import permission_required


# --- Dashboard ---
@permission_required('info_service.view')
def main_page(request):
    """
    Dashboard view showing recent logs and announcements.
    """
    config, _ = InfoServiceConfiguration.objects.get_or_create(user=request.user)
    lastest_logs = Log.objects.order_by('-date')[:config.log_display_limit]
    lastest_announcements = Announcement.objects.order_by('-date')[:config.announcement_display_limit]

    if hasattr(request.user, 'log_settings') and request.user.log_settings.log_info:
        Log.objects.create(user=request.user, action='Przeszedł do Dashboard', type='INFO')

    user_favorites = FavoriteLink.objects.filter(user=request.user)

    return render(request, 'web_service/dashboard.html', {
        'user_favorites': user_favorites,
        'favorite_url_names': [fav.url for fav in user_favorites],
        'favorite_names': [fav.name for fav in user_favorites],
        'info_service_config': config,
        'logs': lastest_logs,
        'lastest_announcements': lastest_announcements,
    })


# --- Konto użytkownika ---
@permission_required('profile.account_settings.change')
def account_settings(request):
    """
    View for updating user profile data.
    """
    user = request.user
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            if hasattr(user, 'log_settings') and user.log_settings.log_warning:
                Log.objects.create(user=user, action='Zmienił dane konta', type='WARNING')
            messages.success(request, 'Twoje ustawienia zostały zapisane.')
            return redirect('account_settings')
    else:
        form = UserSettingsForm(instance=user)
        if hasattr(user, 'log_settings') and user.log_settings.log_info:
            Log.objects.create(user=user, action='Wszedł w dane konta', type='INFO')

    return render(request, 'web_service/profile/account_settings.html', {'form': form})


@permission_required('profile.change_password.change')
def change_password(request):
    """
    Allows user to change their own password.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            if hasattr(user, 'log_settings') and user.log_settings.log_warning:
                Log.objects.create(user=user, action='Zmienił hasło', type='WARNING')
            messages.success(request, 'Hasło zostało pomyślnie zmienione.')
            return redirect('change_password')
        else:
            messages.error(request, 'Popraw błędy w formularzu.')
    else:
        storage = get_messages(request)
        list(storage)  # Wymuszenie wyczyszczenia wiadomości
        form = PasswordChangeForm(user=request.user)

        if hasattr(request.user, 'log_settings') and request.user.log_settings.log_info:
            Log.objects.create(user=request.user, action='Wszedł do modułu Zmiana hasła', type='INFO')

    return render(request, 'web_service/profile/change_password.html', {'form': form})


@permission_required('profile.info_service.configuration.change')
def info_service_configuration(request):
    """
    Edit per-user display settings for the dashboard.
    """
    config, _ = InfoServiceConfiguration.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = InfoServiceConfigurationForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            return redirect('info_service_configuration')
    else:
        form = InfoServiceConfigurationForm(instance=config)

    return render(request, 'web_service/profile/info_service/config_form.html', {
        'form': form,
        'title': 'Konfiguracja Infoserwisu'
    })


# --- Ogłoszenia ---
@permission_required('administration.announcement.view')
def announcement_list(request):
    """
    Paginated list of announcements with per-page settings.
    """
    return _paginated_list_view(
        request=request,
        model=Announcement,
        template='web_service/administration/announcement/announcement_list.html',
        log_action='Uruchomił moduł ogłoszenia',
        log_type='INFO'
    )


@permission_required('administration.announcement.create')
def announcement_create(request):
    """
    Form to create a new announcement.
    """
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()

            if hasattr(request.user, 'log_settings') and request.user.log_settings.log_warning:
                Log.objects.create(
                    user=request.user,
                    action=f'Utworzył ogłoszenie „{announcement.subject}” z datą {announcement.date}',
                    type='WARNING'
                )

            return redirect('announcement_list')
    else:
        form = AnnouncementForm()

    return render(request, 'web_service/administration/announcement/announcement_form.html', {
        'form': form,
        'title': 'Dodaj ogłoszenie'
    })


@permission_required('administration.announcement.edit')
def announcement_edit(request, pk):
    """
    Edit an existing announcement.
    """
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            if hasattr(request.user, 'log_settings') and request.user.log_settings.log_warning:
                Log.objects.create(
                    user=request.user,
                    action=f'Edytował ogłoszenie {announcement.subject}.',
                    type='WARNING'
                )
            return redirect('announcement_list')
    else:
        form = AnnouncementForm(instance=announcement)

    return render(request, 'web_service/administration/announcement/announcement_form.html', {
        'form': form,
        'title': f'Edytuj ogłoszenie: {announcement.subject}'
    })


@permission_required('administration.announcement.delete')
def announcement_delete(request, pk):
    """
    Delete an announcement with confirmation.
    """
    element = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        element.delete()
        if hasattr(request.user, 'log_settings') and request.user.log_settings.log_warning:
            Log.objects.create(
                user=request.user,
                action=f'Usunął ogłoszenie {element.subject} z dnia {element.date}',
                type='WARNING'
            )
        messages.success(request, f'Ogłoszenie \"{element.subject}\" zostało usunięte.')
        return redirect('announcement_list')

    return render(request, 'web_service/administration/announcement/announcement_confirm_delete.html', {
        'element': element
    })


# --- Flagi (Tagi) ---
@permission_required('administration.tag.view')
def tag_list(request):
    return _paginated_list_view(
        request=request,
        model=Tag,
        template='web_service/administration/tags/tag_list.html',
        log_action='Uruchomił moduł Flagi',
        log_type='INFO'
    )


@permission_required('administration.tag.create')
def tag_create(request):
    """
    Create a new tag (color + name).
    """
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            if hasattr(request.user, 'log_settings') and request.user.log_settings.log_warning:
                Log.objects.create(
                    user=request.user,
                    action=f'Utworzył flagę {tag.name} o kolorze {tag.color}',
                    type='WARNING'
                )
            return redirect('tag_list')
    else:
        form = TagForm()

    return render(request, 'web_service/administration/tags/tag_form.html', {
        'form': form,
        'title': 'Dodaj nową flagę'
    })


@permission_required('administration.tag.edit')
def tag_edit(request, pk):
    """
    Edit existing tag.
    """
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            tag = form.save()
            if hasattr(request.user, 'log_settings') and request.user.log_settings.log_warning:
                Log.objects.create(
                    user=request.user,
                    action=f'Edytował flagę {tag.name} o kolorze {tag.color}',
                    type='WARNING'
                )
            return redirect('tag_list')
    else:
        form = TagForm(instance=tag)

    return render(request, 'web_service/administration/tags/tag_form.html', {
        'form': form,
        'title': f'Edytuj flagę: {tag.name}'
    })


@permission_required('administration.tag.delete')
def tag_delete(request, pk):
    """
    Delete tag after confirmation.
    """
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        tag.delete()
        if hasattr(request.user, 'log_settings') and request.user.log_settings.log_warning:
            Log.objects.create(
                user=request.user,
                action=f'Usunął flagę {tag.name} o kolorze {tag.color}',
                type='WARNING'
            )
        messages.success(request, f'Flaga \"{tag.name}\" została usunięta.')
        return redirect('tag_list')

    return render(request, 'web_service/administration/tags/tag_confirm_delete.html', {
        'tag': tag
    })


# --- Logi ---
@permission_required('settings.log.view')
def log_list(request):
    return _paginated_list_view(
        request=request,
        model=Log,
        template='web_service/settings/logs/log_list.html',
        log_action='Uruchomił moduł Dziennik aktywności.',
        log_type='INFO'
    )


# --- Użytkownicy ---
@permission_required('settings.user.view')
def user_list(request):
    return _paginated_list_view(
        request=request,
        model=User,
        template='web_service/settings/users/user_list.html',
        ordering='username',
        log_action='Uruchomił moduł użytkowników',
        log_type='INFO'
    )


@permission_required('settings.user.create')
def user_create(request):
    """
    Create new user with logging config and permissions.
    """
    if request.method == 'POST':
        form = CustomUserCreateForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            if hasattr(request.user, 'log_settings') and request.user.log_settings.log_warning:
                Log.objects.create(user=request.user, action=f'Utworzył użytkownika {user.username}.', type='WARNING')
            messages.success(request, f'Użytkownik \"{user.username}\" został utworzony.')
            return redirect('user_list')
    else:
        form = CustomUserCreateForm()

    return render(request, 'web_service/settings/users/user_form.html', {
        'form': form,
        'title': 'Dodaj użytkownika'
    })


@permission_required('settings.user.edit')
def user_edit(request, pk):
    """
    Edit existing user and their settings.
    """
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = CustomUserEditForm(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            if hasattr(request.user, 'log_settings') and request.user.log_settings.log_warning:
                Log.objects.create(user=request.user, action=f'Edytował użytkownika {user.username}.', type='WARNING')
            messages.success(request, f'Użytkownik \"{user.username}\" został zaktualizowany.')
            return redirect('user_list')
    else:
        form = CustomUserEditForm(instance=user)

    return render(request, 'web_service/settings/users/user_form.html', {
        'form': form,
        'title': f'Edytuj użytkownika: {user.username}'
    })


@permission_required('settings.user.delete')
def user_delete(request, pk):
    """
    Delete user account.
    """
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        username = user.username
        user.delete()
        if hasattr(request.user, 'log_settings') and request.user.log_settings.log_warning:
            Log.objects.create(user=request.user, action=f'Usunął użytkownika {username}.', type='WARNING')
        messages.success(request, f'Użytkownik \"{username}\" został usunięty.')
        return redirect('user_list')

    return render(request, 'web_service/settings/users/user_confirm_delete.html', {
        'element': user
    })


# --- Ulubione ---
@require_POST
@login_required
def toggle_favorite(request):
    """
    Add or remove a favorite link (toggle).
    """
    url = request.POST.get('url')
    name = request.POST.get('name')
    user = request.user

    favorite, created = FavoriteLink.objects.get_or_create(user=user, url=url, name=name)
    if not created:
        favorite.delete()

    return redirect(request.META.get('HTTP_REFERER', '/'))


# --- Obsługa błędu 404 ---
def custom_404_view(request, exception=None):
    """
    Custom handler for 404 errors.
    """
    return render(request, 'errors/404.html', status=404)


# --- Wspólny helper dla widoków listowych z paginacją ---
def _paginated_list_view(request, model, template, ordering='pk', log_action=None, log_type='INFO'):
    settings, _ = UserSilentSettings.objects.get_or_create(user=request.user)
    custom = request.GET.get('custom_per_page')
    selected = request.GET.get('per_page')

    try:
        if custom:
            settings.per_page = int(custom)
            settings.save()
        elif selected:
            settings.per_page = int(selected)
            settings.save()
    except ValueError:
        pass

    per_page = settings.per_page
    elements = model.objects.all().order_by(ordering)
    paginator = Paginator(elements, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if log_action and hasattr(request.user, 'log_settings') and request.user.log_settings.log_info:
        Log.objects.create(user=request.user, action=log_action, type=log_type)

    return render(request, template, {
        'elements': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'paginator': paginator,
        'per_page': per_page,
        'per_page_options': [settings.per_page] + [x for x in [10, 20, 50, 100] if x != settings.per_page],
    })
