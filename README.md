# Тестовое задание - Dima-Tech

FastAPI + Swagger UI (/docs) вместо Sanic, допускается условиями ТЗ.
Конфигурация в JSON-файлах в src/binary_files/ (settings.json для локального
запуска, settings.docker.json для Docker, отличается только хостом БД).

## Тестовые учётные данные

Создаются миграцией Alembic вместе с тестовым счётом пользователя.

| Роль  | Email                  | Пароль        |
|-------|------------------------|---------------|
| User  | new_user@example.com  | password      |
| Admin | user@example.com | password |

## Авторизация в Swagger UI

1. POST /auth/login/user или POST /auth/login/admin с данными из таблицы выше.
2. Скопировать access_token из ответа.
3. Кнопка Authorize (справа вверху /docs), вставить токен.
4. Защищённые эндпоинты становятся доступны, токен подставляется автоматически.

## Вариант 1: Docker Compose

```bash
docker compose up --build
```

## Вариант 2: без Docker

Python 3.12+, локально запущенный PostgreSQL (user=postgres, password=password, база dima_tech, см. src/binary_files/settings.json).

```bash
psql -U postgres -c "CREATE DATABASE dima_tech;"

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

alembic upgrade head

python -m src.main
```

После запуска, любым из вариантов:

API: http://localhost:8888
Swagger UI: http://localhost:8888/docs
