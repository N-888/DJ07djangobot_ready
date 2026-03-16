# Импортируем модуль os, чтобы задать переменную окружения с настройками Django.
import os
# Импортируем фабрику WSGI-приложения Django.
from django.core.wsgi import get_wsgi_application

# Указываем Django, какой файл настроек нужно использовать.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangobot.settings')

# Создаем WSGI-приложение для обычных Python-веб-серверов.
application = get_wsgi_application()