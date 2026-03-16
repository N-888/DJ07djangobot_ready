# Импортируем административную панель Django.
from django.contrib import admin
# Импортируем include, чтобы подключить маршруты из отдельного приложения, и path для описания путей.
from django.urls import include, path

# Описываем все маршруты верхнего уровня проекта.
urlpatterns = [
    # Подключаем стандартную административную панель Django.
    path('admin/', admin.site.urls),
    # Подключаем все API-маршруты нашего приложения telegram_api по префиксу api/.
    path('api/', include('telegram_api.urls')),
]