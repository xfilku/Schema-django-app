from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .forms import UserSettingsForm, TagForm, PhoneContactForm
from .models import Tag, Log, PhoneContact, ContactStatus
from django.core.paginator import Paginator
import openpyxl

# Create your views here.

@login_required
def main_page(request):
    if hasattr(request.user, 'log_settings') and request.user.log_settings.log_info:
        Log.objects.create(
            user=request.user,
            action='Przeszedł do Dashboard',
            type = 'INFO'
        )
    return render(request, 'web_service/dashboard.html')

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
    tags = Tag.objects.all()
    #log
    if hasattr(request.user, 'log_settings') and request.user.log_settings.log_info:
        Log.objects.create(
            user=request.user,
            action=f'Wszedł do modułu Flagi',
            type = 'INFO'
        )

    return render(request, 'web_service/settings/tags/tag_list.html', {'tags': tags})

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

    return render(request, 'web_service/settings/tags/tag_form.html', {'form': form, 'title': 'Dodaj nową flagę'})

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

    return render(request, 'web_service/settings/tags/tag_form.html', {'form': form, 'title': f'Edytuj flagę: {tag.name}'})

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

    return render(request, 'web_service/settings/tags/tag_confirm_delete.html', {'tag': tag})

#logs
@login_required
def log_list(request):
    logs = Log.objects.all()
    paginator = Paginator(logs, 20)  # 20 logów na stronę
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if hasattr(request.user, 'log_settings') and request.user.log_settings.log_info:
        Log.objects.create(
            user=request.user,
            action=f'Uruchomił moduł Dzinnik zdarzeń',
            type = 'INFO'
        )

    return render(request, 'web_service/settings/logs/log_list.html', {
        'logs': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'paginator': paginator,
    })

#phonecontact
#listy
@login_required
def contact_list(request):
    contacts = PhoneContact.objects.select_related('tag', 'user').all()
    if hasattr(request.user, 'log_settings') and request.user.log_settings.log_info:
        Log.objects.create(
            user=request.user,
            action=f'Uruchomił moduł Baza kontaktów',
            type = 'INFO'
        )
    return render(request, 'web_service/contacts/contact_list.html', {'contacts': contacts})

@login_required
def contact_list(request):
    contacts = PhoneContact.objects.select_related('tag', 'user').all()
    if hasattr(request.user, 'log_settings') and request.user.log_settings.log_info:
        Log.objects.create(
            user=request.user,
            action=f'Uruchomił moduł Baza kontaktów',
            type = 'INFO'
        )
    return render(request, 'web_service/contacts/contact_list.html', {'contacts': contacts, 'page_info': "Wszystkie"})

@login_required
def contact_list_new(request):
    contacts = PhoneContact.objects.select_related('tag', 'user').filter(status=ContactStatus.NEW)
    if hasattr(request.user, 'log_settings') and request.user.log_settings.log_info:
        Log.objects.create(
            user=request.user,
            action=f'Uruchomił moduł Kontakty - Nowe',
            type = 'INFO'
        )
    return render(request, 'web_service/contacts/contact_list.html', {'contacts': contacts, 'page_info': "Nowe"})

@login_required
def contact_list_callback(request):
    contacts = PhoneContact.objects.select_related('tag', 'user').filter(status=ContactStatus.CALLBACK)
    if hasattr(request.user, 'log_settings') and request.user.log_settings.log_info:
        Log.objects.create(
            user=request.user,
            action=f'Uruchomił moduł Kontakty - Ponowny kontakt',
            type = 'INFO'
        )
    return render(request, 'web_service/contacts/contact_list.html', {'contacts': contacts, 'page_info': "Ponowny kontakt"})

@login_required
def contact_list_passed(request):
    contacts = PhoneContact.objects.select_related('tag', 'user').filter(status=ContactStatus.PASSED_TO_DEV)
    if hasattr(request.user, 'log_settings') and request.user.log_settings.log_info:
        Log.objects.create(
            user=request.user,
            action=f'Uruchomił moduł Kontakty - Przekazane',
            type = 'INFO'
        )
    return render(request, 'web_service/contacts/contact_list.html', {'contacts': contacts, 'page_info': "Przekazane"})

@login_required
def contact_list_rejected(request):
    contacts = PhoneContact.objects.select_related('tag', 'user').filter(status=ContactStatus.REJECTED)
    if hasattr(request.user, 'log_settings') and request.user.log_settings.log_info:
        Log.objects.create(
            user=request.user,
            action=f'Uruchomił moduł Kontakty - Odrzucone',
            type = 'INFO'
        )
    return render(request, 'web_service/contacts/contact_list.html', {'contacts': contacts, 'page_info': "Odrzucone"})

@login_required
def contact_list_other(request):
    contacts = PhoneContact.objects.select_related('tag', 'user').filter(status=ContactStatus.OTHER)
    if hasattr(request.user, 'log_settings') and request.user.log_settings.log_info:
        Log.objects.create(
            user=request.user,
            action=f'Uruchomił moduł Kontakty - Inne',
            type = 'INFO'
        )
    return render(request, 'web_service/contacts/contact_list.html', {'contacts': contacts, 'page_info': "Inne"})

#akcje
@login_required
def contact_create(request):
    if request.method == 'POST':
        form = PhoneContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            if hasattr(request.user, 'log_settings') and request.user.log_settings.log_warning:
                Log.objects.create(
                    user=request.user,
                    action=f"Dodał nowy kontakt: {contact.company_name} (NIP: {contact.nip})",
                    type = 'WARNING'
                )
            return redirect('contact_list')
    else:
        form = PhoneContactForm()

    return render(request, 'web_service/contacts/contact_form.html', {
        'form': form,
        'title': 'Dodaj nowy kontakt',
    })

@login_required
def contact_edit(request, pk):
    contact = get_object_or_404(PhoneContact, pk=pk)
    if request.method == 'POST':
        form = PhoneContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            if hasattr(request.user, 'log_settings') and request.user.log_settings.log_warning:
                Log.objects.create(
                    user=request.user,
                    action=f"Edytował kontakt: {contact.company_name} (NIP: {contact.nip})",
                    type = 'WARNING'
                )
            return redirect('contact_list')
    else:
        form = PhoneContactForm(instance=contact)
    return render(request, 'web_service/contacts/contact_form.html', {'form': form, 'title': 'Edytuj kontakt'})

@login_required
def contact_delete(request, pk):
    contact = get_object_or_404(PhoneContact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        if hasattr(request.user, 'log_settings') and request.user.log_settings.log_warning:
            Log.objects.create(
                user=request.user,
                action=f"Usunął kontakt: {contact.company_name} (NIP: {contact.nip})",
                type = 'WARNING'
            )
        return redirect('contact_list')
    return render(request, 'web_service/contacts/contact_confirm_delete.html', {'contact': contact})

#export
@login_required
def export_contacts_excel(request):
    contacts = PhoneContact.objects.select_related('tag', 'user').all()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Kontakty"

    headers = ['Firma', 'NIP', 'Miasto', 'Telefon', 'Status', 'Data kontaktu', 'Użytkownik', 'Flaga', 'Notatka']
    ws.append(headers)

    for contact in contacts:
        ws.append([
            contact.company_name,
            contact.nip,
            contact.city,
            contact.phone_number,
            contact.get_status_display(),
            contact.contact_date.strftime("%Y-%m-%d %H:%M"),
            contact.user.username if contact.user else "—",
            contact.tag.name if contact.tag else "—",
            contact.note or "",
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=kontakty.xlsx'

    wb.save(response)
    if hasattr(request.user, 'log_settings') and request.user.log_settings.log_warning:
        Log.objects.create(
            user=request.user,
            action=f"Wyeksportował plik z danymi",
            type = 'WARNING'
        )
    return response