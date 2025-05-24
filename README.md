# User Management API

Приложение для управления пользователями с поддержкой регистрации, аутентификации (JWT), ролей, работы с погодой и интеграцией с базой данных (SQLite/PostgreSQL).

---

## Описание

Этот проект реализует backend-сервис на FastAPI для управления пользователями, ролями и погодой. Включает регистрацию, JWT-аутентификацию, работу с асинхронной БД, тесты и автоматическую проверку через GitHub Actions.

---

## Основные возможности

- Регистрация и аутентификация пользователей (JWT)
- Роли пользователей и разграничение прав
- Асинхронная работа с базой данных (SQLite/PostgreSQL)
- Управление погодой (создание и получение данных)
- REST API с документацией Swagger/OpenAPI
- Миграции базы данных через Alembic
- Покрытие тестами (pytest)
- CI/CD через GitHub Actions

---

## Быстрый старт (локально)

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/cavin1347/user_management.git
   cd user_management
   ```
2. **Установите Poetry:**
   ```bash
   pip install poetry
   ```
3. **Установите зависимости:**
   ```bash
   poetry install
   ```
4. **Создайте и настройте .env (при необходимости):**
   - Пример переменных уже есть в `user_management/.env`
5. **Примените миграции базы данных:**
   ```bash
   poetry run alembic upgrade head
   ```
6. **Запустите приложение:**
   ```bash
   poetry run uvicorn user_management.main:app --reload
   ```
7. **Откройте документацию API:**
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Запуск тестов

Для запуска тестов используйте команду:

```bash
poetry run pytest
```

Тесты автоматически запускаются при каждом push или pull request через GitHub Actions.

---

## Примеры API-запросов

### Регистрация пользователя
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "user1",
  "password": "yourpassword"
}
```

### Получение токена (логин)
```http
POST /auth/token
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=yourpassword
```

### Получение информации о погоде
```http
GET /weather/Test%20City
```

### Добавление данных о погоде
```http
POST /weather/
Content-Type: application/json

{
  "city": "Test City",
  "temperature": 25.5,
  "humidity": 60,
  "description": "Sunny"
}
```

---

## Дополнительно

- [x] Проект публичный и открыт для pull request'ов
- [x] Автоматическая проверка тестов через GitHub Actions
- [x] Совместим с Linux и Windows

### Бейджи статуса (пример)

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/cavin1347/user_management/main.yml?branch=main)
![GitHub last commit](https://img.shields.io/github/last-commit/cavin1347/user_management)

### Лицензия

Проект распространяется под лицензией MIT. Подробнее см. в файле [LICENSE](LICENSE).

---

**Автор:** [cavin1347](https://github.com/cavin1347)

---