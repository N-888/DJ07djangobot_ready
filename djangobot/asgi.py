# Импортируем модуль os, чтобы задать переменную окружения с настройками Django.
import os
# Импортируем фабрику ASGI-приложения Django.
from django.core.asgi import get_asgi_application

# Указываем Django, какой файл настроек нужно использовать.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangobot.settings')

# Создаем ASGI-приложение для серверов, работающих по ASGI-протоколу.
application = get_asgi_application()