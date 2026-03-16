# Импортируем path, чтобы описывать маршруты приложения.
from django.urls import path
# Импортируем функцию представления register_user.
from .views import register_user

# Создаем список маршрутов приложения telegram_api.
urlpatterns = [
    # Подключаем endpoint регистрации пользователя по адресу /api/register/.
    path('register/', register_user, name='register_user'),
]