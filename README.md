Chatty
Соцсеть Chatty

Создана виртуальная среда используя venv
Добавлены необходимые зависимости requirements.txt pip install -r requirements.txt
Установлены библиотеки: FastAPI, SQLAlchemy, Pydantic, Alembic
Создан репозиторий, создана начальная структура исходя из общих принципов архитектуры Добавлены директории app и 
исполнительный файл main.py

3. Модели пользователей и постов (SQLAlchemy) 

Модели и база данных

-models.py:
- Определяет модели данных для таблиц users и posts.
- Использует SQLAlchemy ORM для определения структуры таблиц и их полей.
- Каждая модель соответствует таблице в базе данных и определяет поля:
такие как id, email, password_hash и nickname (users)
такие как  id, user_id, title, content и created_at (posts)
- Используется relationship для установки двусторонней связи между users и posts.
 
-database.py:
- Настраивает подключение к базе данных с
использованием SQLAlchemy.
- Создает сессию для взаимодействия с базой данных.

-db_base.py:
- Использует SQLAlchemy.ext.declarative для импорта Base в models.py



6. Миграции (Alembic)

-alembic.ini и alembic/env.py:
- Конфигурационные файлы для Alembic, инструмента для управления миграциями базы данных.
- alembic.ini содержит основные настройки, такие как путь к скриптам миграций. 
- env.py настраивает окружение для выполнения миграций, подключаясь к базе данных и используя метаданные моделей.
 
- 9014fe920ecd_initial_migration.py:
- Автоматически сгенерированная миграция, которая создает таблицы users и posts в базе данных.
- Содержит команды для создания и удаления таблиц и индексов.
 
- Используемые команды
- alembic init alembic
- создание файла миграции: alembic revision --autogenerate -m "Initial migration"
- применить миграцию: alembic upgrade head