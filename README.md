# AI-маркетолог для Instagram-магазинов

## Описание
Веб-сервис с использованием AI, который автоматически генерирует идеи для публикаций и рекламных кампаний, подбирает хэштеги, визуальные материалы и позволяет публиковать их в соцсети.

## Структура проекта
```
├── backend/           # FastAPI проект
│   ├── app/           # Основная логика приложения
│   ├── tests/         # Тесты
│   └── requirements.txt
├── frontend/          # Vue 3 проект
│   ├── src/           # Исходный код
│   └── package.json
├── shared/            # Общие модели, типы и другие ресурсы
└── README.md
```

## Установка и запуск

### Backend

#### Установка зависимостей
```bash
cd backend
pip install -r requirements.txt
```

#### Запуск сервера
```bash
cd backend
python main.py
```

Сервер будет доступен по адресу: http://localhost:8000

### Frontend

#### Установка зависимостей
```bash
cd frontend
npm install
```

#### Запуск для разработки
```bash
cd frontend
npm run dev
```

Клиент будет доступен по адресу: http://localhost:5173

## API Документация
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

## Основные эндпоинты
- POST /auth/register - Регистрация нового пользователя
- POST /auth/login - Авторизация и получение JWT-токена
- GET /auth/me - Информация о текущем пользователе 