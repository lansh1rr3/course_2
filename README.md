# Отслеживание привычек

REST API Django для отслеживания привычек, основанный на "Атомарных привычках" Джеймса Клира

## Установка

1. Клонируем репозиторий
2. Создаем виртуальную среду: `python -m venv venv`
3. Активируем среду
4. Требования к установке: `pip install -r requirements.txt`
5. Настройте файл .env
6. Запустите миграцию: `python manage.py migrate`
7. Запустите сервер: `python manage.py runserver`

## Производственная настройка

1. Установите PostgreSQL и Redis
2. Настройте .env с производственными настройками
3. Запустите миграцию: `python manage.py migrate`
4. Запустите Redis: `redis-server`
5. Запустите Celery: "celery -A config worker -l info"
6. Запустите Celery Beat: `celery -A config beat -l info`
7. Запустите сервер: "python manage.py runserver`

## Аутентификация

- POST /api/auth/jwt/create/ - Получить пару токенов
- POST /api/auth/jwt/refresh/ - Обновить токен
- Использовать токен на предъявителя в заголовке авторизации

## Структура проекта
- "users/": Управляет профилями пользователей и интеграцией с Telegram
- "habits/": Основные функции отслеживания привычек
- `telegram_bot/`: Обрабатывает уведомления Telegram
- `config/`: Настройки и конфигурация проекта

## Локальная настройка

### Предварительные требования
- Docker
- Docker Compose

### Шаги
1. Клонируем репозиторий:
```bash
git clone https://github.com/lansh1rr3/course_2.git
cd course_2
