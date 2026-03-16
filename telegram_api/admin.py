# Импортируем модуль admin, чтобы зарегистрировать модели в административной панели.
from django.contrib import admin
# Импортируем нашу модель TelegramUser.
from .models import TelegramUser


# Регистрируем модель в админке через декоратор.
@admin.register(TelegramUser)
# Создаем класс настройки отображения модели в административной панели.
class TelegramUserAdmin(admin.ModelAdmin):
    # Указываем поля, которые будут видны в списке объектов.
    list_display = ('id', 'user_id', 'username', 'created_at')
    # Указываем поля, по которым можно искать записи.
    search_fields = ('user_id', 'username')
    # Указываем поле, по которому удобно фильтровать список.
    list_filter = ('created_at',)
    # Делаем поле даты только для чтения в админке.
    readonly_fields = ('created_at',)