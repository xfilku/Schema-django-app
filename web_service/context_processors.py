from .models import FavoriteLink, UserSilentSettings

def user_favorites(request):
    if request.user.is_authenticated:
        favorites = FavoriteLink.objects.filter(user=request.user)
        return {
            'user_favorites': favorites,
            'favorite_url_names': [fav.url for fav in favorites],
            'favorite_names': [fav.name for fav in favorites],
        }
    return {
        'user_favorites': [],
        'favorite_url_names': [],
        'favorite_names' : [],
    }

def per_page_setting(request):
    if request.user.is_authenticated:
        setting = UserSilentSettings.objects.filter(user=request.user).first()
        return {'global_per_page': setting.per_page if setting else 20}
    return {'global_per_page': 20}