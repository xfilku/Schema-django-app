from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from web_service.models import UserPermissions, Announcement, Tag
from datetime import date


class BasePermissionTest(TestCase):
    """
    Base test case class for testing view permissions.
    Sets up a test user and helper methods to assign/revoke permissions and perform GET/POST requests.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # Dummy data for views requiring pk
        self.announcement = Announcement.objects.create(
            subject='Test', message='Test message', date=date.today(), created_by=self.user
        )
        self.tag = Tag.objects.create(name='TestTag', color='#FFFFFF')

    def assign_permission(self, code):
        perms, _ = UserPermissions.objects.get_or_create(user=self.user)
        perms.permissions[code] = True
        perms.save()

    def remove_permission(self, code):
        perms, _ = UserPermissions.objects.get_or_create(user=self.user)
        perms.permissions[code] = False
        perms.save()

    def check_view(self, url_name, perm_code, url_kwargs=None):
        """
        Helper method to test that a view is accessible with the correct permission and forbidden without it.
        """
        if url_kwargs:
            url = reverse(url_name, kwargs=url_kwargs)
        else:
            url = reverse(url_name)

        # With permission
        self.assign_permission(perm_code)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, f"{url_name} should be accessible with permission")

        # Without permission
        self.remove_permission(perm_code)
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'errors/403.html')


class MainPagePermissionTest(BasePermissionTest):
    def test_main_page_permission(self):
        self.check_view('main_page', 'info_service.view')


class AccountSettingsPermissionTest(BasePermissionTest):
    def test_account_settings_permission(self):
        self.check_view('account_settings', 'profile.account_settings.change')


class ChangePasswordPermissionTest(BasePermissionTest):
    def test_change_password_permission(self):
        self.check_view('change_password', 'profile.change_password.change')


class InfoServiceConfigPermissionTest(BasePermissionTest):
    def test_info_service_config_permission(self):
        self.check_view('info_service_configuration', 'profile.info_service.configuration.change')


class AnnouncementListPermissionTest(BasePermissionTest):
    def test_announcement_list_permission(self):
        self.check_view('announcement_list', 'administration.announcement.view')


class AnnouncementCreatePermissionTest(BasePermissionTest):
    def test_announcement_create_permission(self):
        self.check_view('announcement_create', 'administration.announcement.create')


class AnnouncementEditPermissionTest(BasePermissionTest):
    def test_announcement_edit_permission(self):
        self.check_view('announcement_edit', 'administration.announcement.edit', url_kwargs={'pk': self.announcement.pk})


class AnnouncementDeletePermissionTest(BasePermissionTest):
    def test_announcement_delete_permission(self):
        self.check_view('announcement_delete', 'administration.announcement.delete', url_kwargs={'pk': self.announcement.pk})


class TagListPermissionTest(BasePermissionTest):
    def test_tag_list_permission(self):
        self.check_view('tag_list', 'administration.tag.view')


class TagCreatePermissionTest(BasePermissionTest):
    def test_tag_create_permission(self):
        self.check_view('tag_create', 'administration.tag.create')


class TagEditPermissionTest(BasePermissionTest):
    def test_tag_edit_permission(self):
        self.check_view('tag_edit', 'administration.tag.edit', url_kwargs={'pk': self.tag.pk})


class TagDeletePermissionTest(BasePermissionTest):
    def test_tag_delete_permission(self):
        self.check_view('tag_delete', 'administration.tag.delete', url_kwargs={'pk': self.tag.pk})


class LogListPermissionTest(BasePermissionTest):
    def test_log_list_permission(self):
        self.check_view('log_list', 'settings.log.view')


class UserListPermissionTest(BasePermissionTest):
    def test_user_list_permission(self):
        self.check_view('user_list', 'settings.user.view')


class UserCreatePermissionTest(BasePermissionTest):
    def test_user_create_permission(self):
        self.check_view('user_create', 'settings.user.create')


class UserEditPermissionTest(BasePermissionTest):
    def test_user_edit_permission(self):
        self.check_view('user_edit', 'settings.user.edit', url_kwargs={'pk': self.user.pk})


class UserDeletePermissionTest(BasePermissionTest):
    def test_user_delete_permission(self):
        self.check_view('user_delete', 'settings.user.delete', url_kwargs={'pk': self.user.pk})


class ToggleFavoritePermissionTest(BasePermissionTest):
    def test_toggle_favorite_no_permission_needed(self):
        response = self.client.post(reverse('toggle_favorite'), {'url': '/test/', 'name': 'Test'})
        self.assertEqual(response.status_code, 302)

class LoginViewTest(TestCase):
    """
    Test for the login view.
    Ensures that the login page is accessible with GET method.
    """
    def test_login_page_accessible(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form', msg_prefix="Login page should contain a form")


class LogoutViewTest(TestCase):
    """
    Test that logout redirects properly using GET method.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='logoutuser', password='logoutpass')
        self.client.login(username='logoutuser', password='logoutpass')

    def test_logout_redirects(self):
        response = self.client.post(reverse('logout'))
        self.assertIn(response.status_code, [302, 200])
