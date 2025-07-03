"""
Dictionary of custom module-level permissions used across the application.

Each permission code corresponds to a boolean field stored in UserPermissions,
and is used to control access via the `permission_required` decorator or manual checks.

The structure follows the pattern: 'module.action': 'Human-readable description (PL)'
"""

MODULE_PERMISSIONS = {
    # --- Panel ---
    'info_service.view': "Dostęp do wyświetlania panelu",

    # --- Profil użytkownika ---
    'profile.account_settings.change': "Możliwość zmiany ustawień użytkownika",
    'profile.change_password.change': "Możliwość samodzielnego zmiany hasła",
    'profile.info_service.configuration.change': "Dostęp do edycji Panelu",

    # --- Administracja ---
    # Ogłoszenia
    "administration.announcement.view": "Dostęp do przeglądania ogłoszeń",
    "administration.announcement.create": "Możliwość dodawania ogłoszenia",
    "administration.announcement.edit": "Możliwość edytowania ogłoszenia",
    "administration.announcement.delete": "Możliwość usuwania ogłoszenia",

    # Tagi
    "administration.tag.view": "Dostęp do przeglądania listy tagów",
    "administration.tag.create": "Możliwość dodawania tagów",
    "administration.tag.edit": "Możliwość edytowania tagów",
    "administration.tag.delete": "Możliwość usuwania tagów",

    # --- Ustawienia ---
    # Logi
    "settings.log.view": "Dostęp do przeglądania dziennika aktywności",

    # Użytkownicy
    "settings.user.view": "Dostęp do przeglądania listy użytkowników",
    "settings.user.create": "Możliwość dodawania użytkownika",
    "settings.user.edit": "Możliwość edytowania użytkownika",
    "settings.user.delete": "Możliwość usuwania użytkownika",
}
