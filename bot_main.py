# Импортируем модуль os, чтобы читать переменные окружения из .env.
import os
# Импортируем Path, чтобы удобно построить путь к файлу .env.
from pathlib import Path
# Импортируем библиотеку requests для отправки HTTP-запросов в Django API.
import requests
# Импортируем библиотеку telebot для создания Telegram-бота.
import telebot
# Импортируем load_dotenv, чтобы загрузить токен и URL API из файла .env.
from dotenv import load_dotenv
# Импортируем тип Message, чтобы сделать код понятнее и удобнее для подсказок IDE.
from telebot.types import Message

# Определяем корневую папку проекта, где лежит файл .env.
BASE_DIR = Path(__file__).resolve().parent

# Загружаем переменные окружения из файла .env.
load_dotenv(BASE_DIR / '.env')

# Получаем токен Telegram-бота из файла .env.
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Получаем базовый адрес Django API из файла .env.
API_BASE_URL = os.getenv('DJANGO_API_BASE_URL', 'http://127.0.0.1:8000/api')

# Собираем полный адрес endpoint регистрации и на всякий случай убираем лишний слеш в конце базового URL.
REGISTER_URL = f"{API_BASE_URL.rstrip('/')}/register/"

# Проверяем, что токен действительно заполнен, иначе сразу завершаем запуск понятной ошибкой.
if not BOT_TOKEN:
    # Выбрасываем исключение с подсказкой, чтобы пользователь не запускал бота с пустым токеном.
    raise ValueError('В .env не найден TELEGRAM_BOT_TOKEN. Откройте .env и вставьте токен вашего бота от BotFather.')

# Создаем экземпляр Telegram-бота и включаем HTML-разметку для красивых сообщений.
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')


# Подключаем обработчик команды /start.
@bot.message_handler(commands=['start'])
# Создаем функцию, которая будет запускаться, когда пользователь пишет /start.
def start_command(message: Message) -> None:
    # Формируем словарь с данными пользователя, которые нужно отправить в Django API.
    data = {
        # Передаем уникальный Telegram ID пользователя.
        'user_id': message.from_user.id,
        # Передаем username пользователя или пустую строку, если username не задан.
        'username': message.from_user.username or '',
    }

    # Пытаемся отправить POST-запрос на регистрацию в API.
    try:
        # Отправляем JSON в Django API и ставим таймаут, чтобы бот не зависал бесконечно.
        response = requests.post(REGISTER_URL, json=data, timeout=10)
    # Перехватываем сетевые ошибки, например если сервер Django не запущен.
    except requests.RequestException:
        # Сообщаем пользователю, что сервер сейчас недоступен.
        bot.send_message(
            message.chat.id,
            '❌ <b>Не удалось связаться с сервером.</b>\n\nПроверьте, запущен ли Django по адресу из .env.',
        )
        # Завершаем работу функции, чтобы не продолжать обработку.
        return

    # Пытаемся превратить ответ сервера в JSON-словарь.
    try:
        # Сохраняем распарсенный JSON в отдельную переменную.
        response_data = response.json()
    # Перехватываем ошибку, если сервер вернул не JSON.
    except ValueError:
        # Подменяем данные безопасным словарем с текстом ошибки.
        response_data = {'message': 'Сервер вернул ответ в неожиданном формате.'}

    # Проверяем, что пользователь только что был успешно зарегистрирован.
    if response.status_code == 201:
        # Забираем вложенные данные пользователя из JSON-ответа.
        user_data = response_data.get('user', {})
        # Отправляем красивое сообщение об успешной регистрации.
        bot.send_message(
            message.chat.id,
            (
                '✅ <b>Вы успешно зарегистрированы!</b>\n\n'
                f"Ваш внутренний ID в базе: <code>{user_data.get('id')}</code>\n"
                f"Ваш Telegram ID: <code>{user_data.get('user_id')}</code>\n"
                f"Ваш username: <code>{user_data.get('username') or 'не указан'}</code>"
            ),
        )
        # Завершаем работу функции после успешной регистрации.
        return

    # Проверяем, что пользователь уже был зарегистрирован раньше.
    if response.status_code == 200:
        # Забираем вложенные данные пользователя из JSON-ответа.
        user_data = response_data.get('user', {})
        # Сообщаем пользователю, что он уже есть в базе.
        bot.send_message(
            message.chat.id,
            (
                'ℹ️ <b>Вы уже были зарегистрированы ранее.</b>\n\n'
                f"Ваш внутренний ID в базе: <code>{user_data.get('id')}</code>\n"
                f"Ваш Telegram ID: <code>{user_data.get('user_id')}</code>\n"
                f"Ваш username: <code>{user_data.get('username') or 'не указан'}</code>"
            ),
        )
        # Завершаем работу функции после отправки сообщения.
        return

    # Для всех остальных статусов показываем текст ошибки, который прислал сервер.
    bot.send_message(
        message.chat.id,
        (
            '❌ <b>Ошибка регистрации.</b>\n\n'
            f"{response_data.get('message', 'Произошла неизвестная ошибка.')}"
        ),
    )


# Проверяем, что файл запущен напрямую, а не импортирован из другого файла.
if __name__ == '__main__':
    # Пишем в консоль, что бот запущен и готов принимать сообщения.
    print('Telegram-бот запущен и ожидает сообщения...')
    # Запускаем бесконечный опрос Telegram-серверов и автоматически восстанавливаемся после временных сбоев.
    bot.infinity_polling(timeout=10, long_polling_timeout=5)