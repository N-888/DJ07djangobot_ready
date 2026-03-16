# Импортируем модуль os, чтобы получать значения из переменных окружения.
import os
# Импортируем Path, чтобы удобно работать с путями к папкам и файлам проекта.
from pathlib import Path
# Импортируем load_dotenv, чтобы загрузить переменные из файла .env.
from dotenv import load_dotenv

# Вычисляем корневую папку проекта, где лежат manage.py и файл .env.
BASE_DIR = Path(__file__).resolve().parent.parent

# Загружаем переменные окружения из файла .env, расположенного в корне проекта.
load_dotenv(BASE_DIR / '.env')

# Берем SECRET_KEY из .env, а если его нет, подставляем временное значение для локальной разработки.
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-me-in-env')

# Читаем DEBUG из .env и превращаем строку True или False в настоящее булево значение.
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Читаем список разрешенных хостов из .env и превращаем строку через запятую в Python-список.
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# Перечисляем все приложения, которые должны быть подключены в проекте.
INSTALLED_APPS = [
    # Подключаем административную панель Django.
    'django.contrib.admin',
    # Подключаем встроенную систему аутентификации Django.
    'django.contrib.auth',
    # Подключаем систему типов содержимого Django.
    'django.contrib.contenttypes',
    # Подключаем систему сессий Django.
    'django.contrib.sessions',
    # Подключаем систему сообщений Django.
    'django.contrib.messages',
    # Подключаем поддержку статических файлов Django.
    'django.contrib.staticfiles',
    # Подключаем Django REST Framework для создания API.
    'rest_framework',
    # Подключаем наше приложение с API для Telegram-бота.
    'telegram_api',
]

# Перечисляем промежуточные обработчики запросов и ответов.
MIDDLEWARE = [
    # Подключаем базовую защиту Django.
    'django.middleware.security.SecurityMiddleware',
    # Подключаем поддержку сессий.
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Подключаем общие функции обработки запросов.
    'django.middleware.common.CommonMiddleware',
    # Подключаем защиту от CSRF-атак.
    'django.middleware.csrf.CsrfViewMiddleware',
    # Подключаем аутентификацию пользователей.
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # Подключаем систему сообщений.
    'django.contrib.messages.middleware.MessageMiddleware',
    # Подключаем защиту от встраивания сайта в чужие iframe.
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Указываем главный файл маршрутов проекта.
ROOT_URLCONF = 'djangobot.urls'

# Настраиваем шаблоны Django.
TEMPLATES = [
    {
        # Указываем движок шаблонов Django.
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Оставляем список дополнительных папок шаблонов пустым, потому что в этом проекте они не нужны.
        'DIRS': [],
        # Разрешаем искать шаблоны внутри приложений.
        'APP_DIRS': True,
        # Подключаем стандартные обработчики контекста для шаблонов.
        'OPTIONS': {
            # Перечисляем функции, которые будут добавлять переменные в каждый шаблон.
            'context_processors': [
                # Добавляем данные для отладки.
                'django.template.context_processors.debug',
                # Добавляем объект request в шаблоны.
                'django.template.context_processors.request',
                # Добавляем данные о пользователе.
                'django.contrib.auth.context_processors.auth',
                # Добавляем сообщения Django.
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Указываем точку входа WSGI для запуска проекта.
WSGI_APPLICATION = 'djangobot.wsgi.application'

# Настраиваем базу данных проекта.
DATABASES = {
    # Используем базовую базу данных с именем default.
    'default': {
        # Указываем движок SQLite, потому что он прост и идеально подходит для учебного проекта.
        'ENGINE': 'django.db.backends.sqlite3',
        # Указываем путь к файлу базы данных db.sqlite3 в корне проекта.
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Подключаем стандартные валидаторы паролей Django.
AUTH_PASSWORD_VALIDATORS = [
    {
        # Проверяем, чтобы пароль не был слишком похож на данные пользователя.
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # Проверяем минимальную длину пароля.
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        # Проверяем, чтобы пароль не был слишком простым.
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # Проверяем, чтобы пароль не состоял только из цифр.
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Указываем язык интерфейса проекта.
LANGUAGE_CODE = 'ru-ru'

# Указываем временную зону проекта.
TIME_ZONE = 'Europe/Moscow'

# Включаем систему интернационализации Django.
USE_I18N = True

# Включаем поддержку временных зон.
USE_TZ = True

# Указываем URL-префикс для статических файлов.
STATIC_URL = 'static/'

# Указываем тип поля первичного ключа по умолчанию для новых моделей.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настраиваем базовые параметры Django REST Framework.
REST_FRAMEWORK = {
    # Разрешаем API принимать и отдавать JSON по умолчанию.
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    # Разрешаем API читать входящие данные в основных форматах.
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
}