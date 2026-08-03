# Тестовое задание - DimaTech

FastAPI + Swagger UI (/docs) вместо Sanic, допускается условиями ТЗ.
Конфигурация в JSON-файлах в src/binary_files/ (settings.json для локального
запуска, settings.docker.json для Docker, отличается только хостом БД).

## Тестовые учётные данные

Создаются миграцией Alembic вместе с тестовым счётом пользователя.

| Роль  | Email                  | Пароль        |
|-------|------------------------|---------------|
| User  | user@example.com  | password      |
| Admin | admin@example.com | password |

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
sudo -u postgres psql -c "CREATE DATABASE dima_tech;"
sudo sed -i "s/local   all   postgres   peer/local   all   postgres   md5/" /etc/postgresql/*/main/pg_hba.conf
sudo systemctl restart postgresql
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'password';"

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

alembic upgrade head

python -m src.main
```

Swagger UI: http://localhost:8888/docs
