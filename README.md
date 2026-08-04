# Тестовое задание - DimaTech

1) Реализация тестового задания для команды DimaTech.
2) Использовал FastAPI с использованием Swagger UI.
3) Добавлены инструкции для деплоя как в Docker Compose так и локально.
4) Файл с настройками проекта (.env) был добавлен в публичный репозиторий НАМЕРЕННО, что бы быстро проверить работоспособность проекта.
5) Заполнения тестовыми данными реализованы реализованы через незащищенный эндпоинт /seed/test-data.

## Тестовые учётные данные

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

## Вариант 2: без Docker (Для Ubuntu)

Python 3.12+, локально запущенный PostgreSQL (user=postgres, password=password, база dima_tech, см. конфигурацию проекта).
Первые 4 операции - создание и настройка базы данных.
Операции 5 и 6 - настройка виртуального окружения для Python.
Операция 7 - скачивание зависимостей в виртуальное окружение проекта.
Операция 8 - применение миграций к созданной базе данных.
Операция 9 - запуск сервера с приложением.

```bash
1) sudo -u postgres psql -c "CREATE DATABASE dima_tech;"
2) sudo sed -i "s/local   all   postgres   peer/local   all   postgres   md5/" /etc/postgresql/*/main/pg_hba.conf
3) sudo systemctl restart postgresql
4) sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'password';"

5) python -m venv .venv
6) source .venv/bin/activate

7) pip install -r requirements.txt

8) alembic upgrade head

9) python -m src.main
```

Swagger UI: http://localhost:8888/docs (Вместо 8888 ставим порт на котором запущен сервер с приложением)
