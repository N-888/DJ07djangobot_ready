# Импортируем статус-коды HTTP, чтобы возвращать правильные ответы API.
from rest_framework import status
# Импортируем декоратор api_view, чтобы ограничить представление только POST-запросами.
from rest_framework.decorators import api_view
# Импортируем Response, чтобы красиво возвращать JSON-ответы.
from rest_framework.response import Response
# Импортируем модель TelegramUser.
from .models import TelegramUser
# Импортируем сериализатор TelegramUserSerializer.
from .serializers import TelegramUserSerializer


# Разрешаем этому представлению принимать только POST-запросы.
@api_view(['POST'])
# Создаем функцию регистрации пользователя, которую будет вызывать Telegram-бот.
def register_user(request):
    # Создаем сериализатор на основе пришедших данных для валидации user_id и username.
    serializer = TelegramUserSerializer(data=request.data)

    # Проверяем, что входящие данные корректны.
    if not serializer.is_valid():
        # Возвращаем JSON с ошибками валидации и кодом 400 Bad Request.
        return Response(
            {
                'success': False,
                'message': 'Переданы некорректные данные.',
                'errors': serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Забираем Telegram ID из уже проверенных данных.
    user_id = serializer.validated_data['user_id']
    # Забираем username из проверенных данных или подставляем пустую строку, если username отсутствует.
    username = serializer.validated_data.get('username') or ''

    # Пытаемся получить пользователя из базы, а если его нет, создаем новую запись.
    user, created = TelegramUser.objects.get_or_create(
        # Ищем пользователя по уникальному Telegram ID.
        user_id=user_id,
        # Если записи еще нет, создаем ее с указанным username.
        defaults={'username': username},
    )

    # Если пользователь уже существовал, но теперь у него появился или изменился username, обновляем его.
    if not created and username and user.username != username:
        # Записываем новый username в объект.
        user.username = username
        # Сохраняем только поле username, чтобы не делать лишних изменений.
        user.save(update_fields=['username'])

    # Сериализуем уже сохраненного пользователя для ответа клиенту.
    response_serializer = TelegramUserSerializer(user)

    # Если пользователь был создан впервые, возвращаем код 201 Created.
    if created:
        # Отдаем успешный JSON-ответ для нового пользователя.
        return Response(
            {
                'success': True,
                'message': 'Пользователь успешно зарегистрирован.',
                'user': response_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    # Если пользователь уже существовал, возвращаем код 200 OK.
    return Response(
        {
            'success': True,
            'message': 'Пользователь уже был зарегистрирован ранее.',
            'user': response_serializer.data,
        },
        status=status.HTTP_200_OK,
    )