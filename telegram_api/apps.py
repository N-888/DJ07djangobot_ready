# Импортируем базовый класс конфигурации приложения Django.
from django.apps import AppConfig


# Создаем конфигурацию нашего приложения telegram_api.
class TelegramApiConfig(AppConfig):
    # Указываем тип поля первичного ключа по умолчанию.
    default_auto_field = 'django.db.models.BigAutoField'
    # Указываем системное имя приложения.
    name = 'telegram_api'
    # Указываем человекочитаемое название приложения.
    verbose_name = 'Telegram API'