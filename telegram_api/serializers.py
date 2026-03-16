# Импортируем serializers из Django REST Framework, чтобы валидировать и сериализовать данные.
from rest_framework import serializers
# Импортируем модель TelegramUser, с которой будет работать сериализатор.
from .models import TelegramUser


# Создаем сериализатор для проверки входящих данных и подготовки JSON-ответа.
class TelegramUserSerializer(serializers.ModelSerializer):
    # Описываем внутренние настройки сериализатора.
    class Meta:
        # Указываем модель, для которой создается сериализатор.
        model = TelegramUser
        # Указываем, какие поля будут доступны через API.
        fields = ('id', 'user_id', 'username', 'created_at')
        # Указываем поля, которые нельзя передавать на создание вручную.
        read_only_fields = ('id', 'created_at')