from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .forms import UserSettingsForm, TagForm, InfoServiceConfigurationForm, AnnouncementForm, CustomUserCreateForm, CustomUserEditForm
from .models import Tag, Log, FavoriteLink, UserSilentSettings, InfoServiceConfiguration, Announcement
from django.core.paginator import Paginator

@login_required
def main_page(request):
    config, _ = InfoServiceConfiguration.objects.get_or_create(user=request.user)
    lastest_logs = Log.objects.order_by('-date')[:config.log_display_limit]
    lastest_announcements = Announcement.objects.order_by('-date')[:config.announcement_display_limit]

    # Logowanie aktywności (jeśli ustawienia na to pozwalają)
    if hasattr(request.user, 'log_settings') and request.user.log_settings.log_info:
        Log.objects.create(
            user=request.user,
            action='Przeszedł do Dashboard',
            type='INFO'
        )

    # Pobranie ulubionych zakładek użytkownika
    user_favorites = FavoriteLink.objects.filter(user=request.user)
    favorite_url_names = [fav.url for fav in user_favorites]
    favorite_names = [fav.name for fav in user_favorites]

    # Przekazanie danych do szablonu
    return render(request, 'web_service/dashboard.html', {
        'user_favorites': user_favorites,
        'favorite_url_names': favorite_url_names,
        'favorite_names': favorite_names,
        'info_service_config': config,
        'logs': lastest_logs,
        'lastest_announcements': lastest_announcements,
    })


@login_required
def account_settings(request):
    user = request.user
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            if hasattr(request.user, 'log_settings') and request.user.log_settings.log_warning:
                Log.objects.create(
                    user=request.user,
                    action='Zmienił dane konta',
                    type = 'WARNING'
                )
            messages.success(request, 'Twoje ustawienia zostały zapisane.')
            return redirect('account_settings')
    else:
        form = UserSettingsForm(instance=user)
        if hasattr(request.user, 'log_settings') and request.user.log_settings.log_info:
            Log.objects.create(
                user=request.user,
                action='Wszedł w dane konta',
                type = 'INFO'
            )
    return render(request, 'web_service/profile/account_settings.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            if hasattr(request.user, 'log_settings') and request.user.log_settings.log_warning:
                Log.objects.create(
                    user=request.user,
                    action='Zmienił hasło',
                    type = 'WARNING'
                )
            update_session_auth_hash(request, user)  # Zapobiega wylogowaniu
            messages.success(request, 'Hasło zostało pomyślnie zmienione.')
            return redirect('change_password')
        else:
            messages.error(request, 'Popraw błędy w formularzu.')
    else:
        form = PasswordChangeForm(user=request.user)
        if hasattr(request.user, 'log_settings') and request.user.log_settings.log_info:
            Log.objects.create(
                user=request.user,
                action='Wszedł do modułu Zmiana hasła',
                type = 'INFO'
            )
    return render(request, 'web_service/profile/change_password.html', {'form': form})

#tags
@login_required
def tag_list(request):
    """
    Widok listy tagów z obsługą paginacji i ustawieniem liczby rekordów na stronę przechowywanym w UserSilentSettings.
    """
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
    elements = Tag.objects.all().order_by('name')
    paginator = Paginator(elements, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if hasattr(request.user, 'log_settings') and request.user.log_settings.log_info:
        Log.objects.create(
            user=request.user,
            action='Uruchomił moduł Flagi',
            type='INFO'
        )

    return render(request, 'web_service/administration/tags/tag_list.html', {
        'elements': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'paginator': paginator,
        'per_page': per_page,
        'per_page_options': [settings.per_page] + [x for x in [10, 20, 50, 100] if x != settings.per_page],
    })

@login_required
def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            #log
            if hasattr(request.user, 'log_settings') and request.user.log_settings.log_warning:
                Log.objects.create(
                    user=request.user,
                    action=f'Utworzył flagę {tag.name} o kolorze {tag.color}',
                    type = 'WARNING'
                )
            return redirect('tag_list')
    else:
        form = TagForm()

    return render(request, 'web_service/administration/tags/tag_form.html', {'form': form, 'title': 'Dodaj nową flagę'})

@login_required
def tag_edit(request, pk):
    tag = get_object_or_404(Tag, pk=pk)

    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            tag = form.save()
            #log
            if hasattr(request.user, 'log_settings') and request.user.log_settings.log_warning:
                Log.objects.create(
                    user=request.user,
                    action=f'Edytował flagę {tag.name} o kolorze {tag.color}',
                    type = 'WARNING'
                )
            return redirect('tag_list')
    else:
        form = TagForm(instance=tag)

    return render(request, 'web_service/administration/tags/tag_form.html', {'form': form, 'title': f'Edytuj flagę: {tag.name}'})

@login_required
def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk)

    if request.method == 'POST':
        #log
        tag.delete()
        if hasattr(request.user, 'log_settings') and request.user.log_settings.log_warning:
            Log.objects.create(
                user=request.user,
                action=f'Usunął flagę {tag.name} o kolorze {tag.color}',
                type = 'WARNING'
            )
        messages.success(request, f'Flaga "{tag.name}" została usunięta.')
        return redirect('tag_list')

    return render(request, 'web_service/administration/tags/tag_confirm_delete.html', {'tag': tag})

#logs
@login_required
def log_list(request):
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
    elements = Log.objects.all()
    paginator = Paginator(elements, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if hasattr(request.user, 'log_settings') and request.user.log_settings.log_info:
        Log.objects.create(
            user=request.user,
            action='Uruchomił moduł Dziennik aktywności.',
            type='INFO'
        )

    return render(request, 'web_service/settings/logs/log_list.html', {
        'elements': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'paginator': paginator,
        'per_page': per_page,
        'per_page_options': [settings.per_page] + [x for x in [10, 20, 50, 100] if x != settings.per_page],
    })

#fav
@require_POST
@login_required
def toggle_favorite(request):
    url = request.POST.get('url')
    name = request.POST.get('name')
    user = request.user

    favorite, created = FavoriteLink.objects.get_or_create(user=user, url=url, name=name)
    if not created:
        favorite.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

#infopage settings

@login_required
def info_service_configuration(request):
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

@login_required
def announcement_list(request):
    """
    Widok listy tagów z obsługą paginacji i ustawieniem liczby rekordów na stronę przechowywanym w UserSilentSettings.
    """
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
    elements = Announcement.objects.all().order_by('created_by')
    paginator = Paginator(elements, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if hasattr(request.user, 'log_settings') and request.user.log_settings.log_info:
        Log.objects.create(
            user=request.user,
            action='Uruchomił moduł ogłoszenia',
            type='INFO'
        )

    return render(request, 'web_service/administration/announcement/announcement_list.html', {
        'elements': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'paginator': paginator,
        'per_page': per_page,
        'per_page_options': [settings.per_page] + [x for x in [10, 20, 50, 100] if x != settings.per_page],
    })

@login_required
def announcement_create(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()

            # logowanie utworzenia ogłoszenia
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

@login_required
def announcement_edit(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            announcement = form.save()
            #log
            if hasattr(request.user, 'log_settings') and request.user.log_settings.log_warning:
                Log.objects.create(
                    user=request.user,
                    action=f'Edytował ogłoszenie {announcement.subject}.',
                    type = 'WARNING'
                )
            return redirect('announcement_list')
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'web_service/administration/announcement/announcement_form.html', {'form': form, 'title': f'Edytuj ogłoszenie: {announcement.subject}'})

@login_required
def announcement_delete(request, pk):
    element = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        #log
        element.delete()
        if hasattr(request.user, 'log_settings') and request.user.log_settings.log_warning:
            Log.objects.create(
                user=request.user,
                action=f'Usunął ogłoszenie {element.subject} z dnia {element.date}',
                type = 'WARNING'
            )
        messages.success(request, f'Ogłoszenie "{element.subject}" zostało usunięte.')
        return redirect('announcement_list')

    return render(request, 'web_service/administration/announcement/announcement_confirm_delete.html', {'element': element})

@login_required
def user_list(request):
    """
    Widok listy użytkowników z paginacją i ustawieniami per_page zapisanymi w UserSilentSettings.
    """
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
    elements = User.objects.all().order_by('username')

    paginator = Paginator(elements, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # logowanie wejścia
    if hasattr(request.user, 'log_settings') and request.user.log_settings.log_info:
        Log.objects.create(
            user=request.user,
            action='Uruchomił moduł użytkowników',
            type='INFO'
        )

    return render(request, 'web_service/settings/users/user_list.html', {
        'elements': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'paginator': paginator,
        'per_page': per_page,
        'per_page_options': [settings.per_page] + [x for x in [10, 20, 50, 100] if x != settings.per_page],
    })

def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()

            # log
            if hasattr(request.user, 'log_settings') and request.user.log_settings.log_warning:
                Log.objects.create(
                    user=request.user,
                    action=f'Utworzył użytkownika {user.username}.',
                    type='WARNING'
                )

            messages.success(request, f'Użytkownik "{user.username}" został utworzony.')
            return redirect('user_list')
    else:
        form = CustomUserCreateForm()

    return render(request, 'web_service/settings/users/user_form.html', {
        'form': form,
        'title': 'Dodaj użytkownika'
    })

@login_required
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()

            if hasattr(request.user, 'log_settings') and request.user.log_settings.log_warning:
                Log.objects.create(
                    user=request.user,
                    action=f'Edytował użytkownika {user.username}.',
                    type='WARNING'
                )

            messages.success(request, f'Użytkownik "{user.username}" został zaktualizowany.')
            return redirect('user_list')
    else:
        form = CustomUserEditForm(instance=user)

    return render(request, 'web_service/settings/users/user_form.html', {
        'form': form,
        'title': f'Edytuj użytkownika: {user.username}'
    })

@login_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        username = user.username
        user.delete()

        if hasattr(request.user, 'log_settings') and request.user.log_settings.log_warning:
            Log.objects.create(
                user=request.user,
                action=f'Usunął użytkownika {username}.',
                type='WARNING'
            )

        messages.success(request, f'Użytkownik "{username}" został usunięty.')
        return redirect('user_list')

    return render(request, 'web_service/settings/users/user_confirm_delete.html', {
        'element': user  # dla spójności z template
    })