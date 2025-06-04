from django.urls import path, include
from .views import main_page, account_settings, change_password
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', main_page, name='main_page'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account/settings/', account_settings, name='account_settings'),
    path('change-password/', change_password, name='change_password'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
