# Backend Сервис

## Настройка базы данных и миграций

В проекте используется PostgreSQL в качестве основной базы данных и Alembic для управления миграциями.

### Первоначальная настройка

1. Установите PostgreSQL и создайте базу данных:
   ```bash
   createuser postgres -s
   createdb -U postgres marketolog_db
   ```

2. Настройте переменные окружения в файле `.env`:
   ```
   DATABASE_URL="postgresql://postgres:postgres@localhost:5432/marketolog_db"
   ```

### Выполнение миграций

Для применения миграций к базе данных:

```bash
cd backend
alembic -c migrations/alembic.ini upgrade head
```

### Создание новых миграций

При изменении моделей для автоматического создания новых миграций:

```bash
cd backend
alembic -c migrations/alembic.ini revision --autogenerate -m "описание изменений"
```

### Откат миграций

Для отката последней миграции:

```bash
cd backend
alembic -c migrations/alembic.ini downgrade -1
```

### Проверка текущего статуса миграций

```bash
cd backend
alembic -c migrations/alembic.ini current
```

### Просмотр истории миграций

```bash
cd backend
alembic -c migrations/alembic.ini history
``` 