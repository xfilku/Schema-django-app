from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserSettingsForm
# Create your views here.

@login_required
def main_page(request):
    return render(request, 'web_service/dashboard.html')

@login_required
def account_settings(request):
    user = request.user
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Twoje ustawienia zostały zapisane.')
            return redirect('account_settings')
    else:
        form = UserSettingsForm(instance=user)
    return render(request, 'web_service/account_settings.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Zapobiega wylogowaniu
            messages.success(request, 'Hasło zostało pomyślnie zmienione.')
            return redirect('change_password')
        else:
            messages.error(request, 'Popraw błędy w formularzu.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'web_service/change_password.html', {'form': form})