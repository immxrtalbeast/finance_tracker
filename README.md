Finance Tracker (FastAPI)
=========================

Небольшой сервис, чтобы освоиться на FastAPI с многослойной архитектурой (domain → application services → infrastructure) для пользователей, счетов и транзакций.

Стек
- FastAPI, Pydantic v2
- SQLAlchemy 2.0 async + asyncpg/psycopg
- Alembic для миграций
- Аутентификация: JWT в httponly cookie, passlib/argon2
- Docker / docker-compose (Postgres, Redis, Adminer)
- uv для управления зависимостями

Структура
- `src/main.py` — инициализация приложения, CORS, обработчики исключений.
- `src/presentation/api/` — роутеры и зависимости.
- `src/application/services/` — бизнес-логика; транзакции через Unit of Work.
- `src/domain/` — сущности, ORM-модели, интерфейсы репозиториев, ошибки.
- `src/infrastructures/db/` — реализации репозиториев.
- `src/infrastructures/uow/` — Unit of Work для SQLAlchemy.
- `src/utils/` — движок/сессия БД, JWT-утилиты.
- `src/migrations/` — Alembic.

Окружение в .env.example

Установка и запуск (uv)
```bash
uv sync --frozen
uv run alembic upgrade head
uv run uvicorn src.main:app --host 0.0.0.0 --port ${APP_PORT:-8000}
```

Docker
- Копируйте docker-compose.yml + напишите .env по .env.example
- `docker-compose pull`
- `docker-compose run`
- FastAPI контейнер выполнит миграции и запустится на порту из .env.

Аутентификация
- `POST /users/login` устанавливает `access_token` в httponly cookie.
- Защищённые эндпоинты используют зависимость `current_user_id` (читается из cookie) и проверяют владение ресурсами.

Базовые эндпоинты
- `POST /users` — регистрация.
- `POST /users/login` — вход, установка JWT cookie.
- `GET/DELETE /users/{id}` — только для себя.
- `POST/GET/DELETE/PATCH /accounts...` — только владелец.
- `POST/GET/DELETE /transactions...` — только владелец; обновление баланса атомарно (UoW).
- `GET /health` — проверка здоровья.

Заметки / TODO
- Добавить пагинацию/фильтры для списков, кэширование (Redis), учесть CSRF для cookie-авторизации.
- Доп. ручки для полноценного CRUD`а