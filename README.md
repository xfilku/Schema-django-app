# 🛡️ Django Permissions & Info Panel System

System zarządzania panelem informacyjnym i kontrolą dostępu oparty na niestandardowych uprawnieniach użytkownika.

## 📦 Zawartość projektu

- **Moduł uprawnień**: System `UserPermissions` pozwalający przypisywać granularne uprawnienia do konkretnych funkcji aplikacji.
- **Panele administracyjne**: Zarządzanie ogłoszeniami, użytkownikami, tagami i ustawieniami.
- **Konfiguracja panelu użytkownika**: Spersonalizowane ustawienia wyświetlania danych na stronie głównej.
- **Ulubione linki**: System dodawania i usuwania ulubionych zakładek dla każdego użytkownika.
- **System logowania akcji**: Przechowywanie dziennika zdarzeń użytkownika.
- **Testy jednostkowe**: Pełne pokrycie testami widoków w zależności od uprawnień, testy logiki modeli i sygnałów.

## 🚀 Jak uruchomić

Aby uruchomić projekt lokalnie:

### 1. Sklonuj repozytorium

```bash
git clone https://github.com/xfilku/Schema-django-app.git
cd Schema-django-app
```

### 2. Utwórz i aktywuj wirtualne środowisko

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Zainstaluj zależności

```bash
pip install -r requirements.txt
```

### 4. Utwórz plik `.env`

W katalogu głównym (tam gdzie `manage.py`) utwórz plik `.env` z taką zawartością:

```
DJANGO_SECRET_KEY=tu-wklej-wlasny-klucz
```

🔑 Aby wygenerować bezpieczny klucz:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

> Plik `.env` znajduje się w `.gitignore`, więc nie zostanie przypadkowo opublikowany.

### 5. Uruchom aplikację

```bash
python manage.py runserver
```

Baza danych `db.sqlite3` zawiera przykładowe dane, więc nie trzeba tworzyć konta superużytkownika.

### ✅ Gotowe!

Aplikacja będzie dostępna pod adresem:  
[http://127.0.0.1:8000](http://127.0.0.1:8000)

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

## License

This project is licensed under a **Custom Non-Commercial License**.
You may use, modify, and share the code freely for personal and non-commercial use.

➡️ Commercial use requires a license. Contact me at: 1j51.dyszkiewicz@gmail.com  
See [LICENSE](LICENSE) for full terms.

Projekt objęty jest licencją Custom Non-Commercial License (niestandardowa licencja niekomercyjna).
Wolno: używać, modyfikować i udostępniać ten kod w celach edukacyjnych, prywatnych i niekomercyjnych.
Nie wolno: używać kodu do celów komercyjnych (sprzedaż, wykorzystanie w płatnych produktach), sprzedawać ani redystrybuować całości lub fragmentów, nawet po modyfikacji.

➡️ W przypadku chęci komercyjnego wykorzystania napisz do autora: 1j51.dyszkiewicz@gmail.com
Sprawdź [LICENSE](LICENSE) i poznaj pełne warunki licencji.
