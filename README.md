# ChatJPG - проект на базе Chainlit + FastAPI.

#### Версия разработки: Python 3.12
#### Инструменты разработки: Chainlit, FastAPI, sqlalchemy (ORM, +asyncpg), alembic, Redis, PyJWT, PyTest
#### CI/CD стек: Docker, git

Модуль логирования: ```src/utils/log.py (Хранение в src/files)```

## Инструкция по запуску проекта:
1. **Скопируйте репозиторий на локальную машину:**
    - ```git clone https://github.com/Jeson3532/ChatLLMA.git```
2. **Создайте и активируйте виртуальное окружение:**
    - ```python -m venv .venv``` | ```py -m venv .venv```
    - ```source .venv/bin/activate (Linux)``` | ```./.venv/Scripts/activate (PS)```
3. **Установите все зависимости на локальную машину:**
    - ```pip install -r requirements.txt```
4. **Установите PYTHONPATH на корень проекта:**
    - PS: ```$env:PYTHONPATH='.'```
    - CMD: ```set PYTHONPATH=.```
    - Linux & macOS: ```export PYTHONPATH=.```
4. **Установите и запустите Docker:**
    - Windows: установите Docker Desktop и активируйте компонент WSL на компьютере, после запустите его.
    - macOS: установите Docker Desktop и запустите его.
    - Linix: Установите Docker Engine через официальный репозиторий и запустите процесс.
5. **Установите модель LLAMA3 в сервисе ollama:**
   - ```docker exec -it chatllma-ollama-1 ollama pull llama3```
6. **Загрузите все миграции:**
   - ```docker exec -it chatllma-postgres_db-1 alembic upgrade head```
7. **Выполните команды для запуска контейнера:**
    - ```docker compose up -d --build```
8. **Подключитесь к ветке localhost/assistant для получения доступа к ассистенту. (перед этим нужно зарегаться по ручке localhost/auth/register)**