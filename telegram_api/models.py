# Импортируем модуль models, чтобы описывать таблицы базы данных через классы Django.
from django.db import models


# Создаем модель для хранения пользователей, пришедших из Telegram-бота.
class TelegramUser(models.Model):
    # Сохраняем Telegram ID пользователя и запрещаем дубликаты.
    user_id = models.BigIntegerField(unique=True, verbose_name='Telegram ID')
    # Сохраняем username пользователя и разрешаем пустое значение, если username у него отсутствует.
    username = models.CharField(max_length=255, blank=True, null=True, verbose_name='Username')
    # Автоматически записываем дату и время создания записи.
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    # Определяем красивое текстовое представление объекта в админке и консоли.
    def __str__(self) -> str:
        # Возвращаем username и Telegram ID, чтобы запись было удобно распознавать.
        return f'{self.username or "без username"} ({self.user_id})'

    # Создаем дополнительные настройки модели.
    class Meta:
        # Указываем имя модели в единственном числе для админки.
        verbose_name = 'Пользователь Telegram'
        # Указываем имя модели во множественном числе для админки.
        verbose_name_plural = 'Пользователи Telegram'
        # Указываем сортировку по более новым пользователям сверху.
        ordering = ['-created_at']