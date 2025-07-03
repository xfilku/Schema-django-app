# 🛡️ Django Permissions & Info Panel System

System zarządzania panelem informacyjnym i kontrolą dostępu oparty na niestandardowych uprawnieniach użytkownika.

## 📦 Zawartość projektu

- **Moduł uprawnień**: System `UserPermissions` pozwalający przypisywać granularne uprawnienia do konkretnych funkcji aplikacji.
- **Panele administracyjne**: Zarządzanie ogłoszeniami, użytkownikami, tagami i ustawieniami.
- **Konfiguracja panelu użytkownika**: Spersonalizowane ustawienia wyświetlania danych na stronie głównej.
- **Ulubione linki**: System dodawania i usuwania ulubionych zakładek dla każdego użytkownika.
- **System logowania akcji**: Przechowywanie dziennika zdarzeń użytkownika.
- **Testy jednostkowe**: Pełne pokrycie testami widoków w zależności od uprawnień, testy logiki modeli i sygnałów.

## 🚀 Jak uruchomić projekt

### 1. Instalacja zależności

```bash
pip install -r requirements.txt
```

### 2. Migracje i uruchomienie serwera

```bash
python manage.py migrate
python manage.py runserver
```

### 3. Uruchamianie testów

#### ✅ Wszystkie testy

```bash
python manage.py test web_service
```

#### ✅ Jeden test

```bash
python manage.py test web_service.tests.PermissionTests.test_user_has_access_to_dashboard
```

## ✅ Testy jednostkowe

Znajdują się w pliku: `web_service/tests.py`

### Pokrywane testy:

- Dostęp do każdego widoku z uprawnieniami i bez nich (kod 200 / błąd 403)
- Tworzenie relacji `UserLogSettings`, `UserSilentSettings`, `UserPermissions` przy tworzeniu użytkownika
- Dodawanie/usuwanie ulubionych linków
- Sprawdzenie działania `has_permission`
- Testy metod `__str__`

## 🔑 Lista uprawnień (przykłady)

| Kod uprawnienia                           | Opis                                       |
|-------------------------------------------|--------------------------------------------|
| `info_service.view`                       | Dostęp do dashboardu                       |
| `administration.announcement.create`      | Dodawanie ogłoszenia                       |
| `settings.user.edit`                      | Edytowanie użytkowników                    |
| `profile.account_settings.change`         | Edytowanie ustawień konta                 |

Pełna lista: `web_service/permissions.py`

## 🧪 Przykład testu

```python
def test_user_has_all_permissions(self):
    for code in MODULE_PERMISSIONS:
        self.assertTrue(self.user.custom_permissions.has_permission(code))
```

## 📁 Struktura aplikacji

```
web_service/
├── models.py
├── views.py
├── urls.py
├── permissions.py
├── tests.py
├── signals.py
```

## 📌 Uwagi

- Widoki są zabezpieczone dekoratorem `@permission_required`
- Uprawnienia są przechowywane w modelu `UserPermissions` jako pole JSON
- Sygnały automatycznie tworzą domyślne konfiguracje dla użytkownika

## 👤 Użytkownicy
- login: f-dyszk, hasło: tajnehaslo123 (superadmin)
- login: j-kowalski, hasło: tajnehaslo321 (zwykły użytkownik)

## ✍️ Autor

Projekt stworzony przez **Filipa Dyszkiewicza** jako rozbudowany system panelu zarządzania z testami i kontrolą dostępu.