from django.urls import path
from .views import main_page, account_settings, change_password, tag_list, tag_edit,tag_create, tag_delete, log_list, toggle_favorite
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', main_page, name='main_page'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    #acc
    path('account/settings/', account_settings, name='account_settings'),
    path('change-password/', change_password, name='change_password'),
    #settings
    #flag
    path('tags/', tag_list, name='tag_list'),
    path('tags/create/', tag_create, name='tag_create'),  
    path('tags/<int:pk>/edit/', tag_edit, name='tag_edit'),  
    path('tags/<int:pk>/delete/', tag_delete, name='tag_delete'),  
    #logs
    path('logs/', log_list, name='log_list'),
    #phonecontacts
    path('toggle-favorite/', toggle_favorite, name='toggle_favorite'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
