from django.urls import path
from .views import main_page, account_settings, change_password, tag_list, tag_edit,tag_create, tag_delete, log_list, contact_list, contact_create, contact_delete, contact_edit, contact_list_callback, contact_list_new, contact_list_other, contact_list_passed, contact_list_rejected, export_contacts_excel
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
    path('contacts/', contact_list, name='contact_list'),
    path('contacts-new/', contact_list_new, name='contact_list_new'),
    path('contacts-callback/', contact_list_callback, name='contact_list_callback'),
    path('contacts-passed/', contact_list_passed, name='contact_list_passed'),
    path('contacts-rejected/', contact_list_rejected, name='contact_list_rejected'),
    path('contacts-other/', contact_list_other, name='contact_list_other'),
    #phonecontacts-actions
    path('contacts/add/', contact_create, name='contact_create'),
    path('contacts/<int:pk>/edit/', contact_edit, name='contact_edit'),
    path('contacts/<int:pk>/delete/', contact_delete, name='contact_delete'),
    #eksport z excela
    path('contacts/export/', export_contacts_excel, name='contacts_export'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
