## Требования
- Python 3.12+
- Docker (по желанию)
- Установленная Ollama (локально или доступная по сети)

## Установка Ollama (Linux)
```shell
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
ollama pull <модель для эмбединга>
ollama pull <модель для генерации>
```

## Команды бота
- **/start** — старт
- **/chunks** — текущие чанки документа
- **/search <текст>** — поиск по векторной базе
- **<текст>** — ответ с использованием векторной базы
- **<документ>** — загрузить документ в векторную базу

## Быстрый старт (Docker Compose)
1) Скопируйте файл `env` в `.env` и заполните переменные
```
APP_BOT_TOKEN=<токен бота>
APP_PROMPT=<необязательно>
APP_DEFAULT_DOC_FILE_PATH=test.txt

OLLAMA_HOST=http://host.docker.internal:11434  # или http://localhost:11434
LANGGRAPH_LANGUAGE_MODEL=<модель LLM>
LANGGRAPH_EMBEDDING_MODEL=<модель эмбеддингов>
LANGGRAPH_TEMPERATURE=0.0
LANGGRAPH_SIMILARITY_SEARCH_K=3
LANGGRAPH_SEPARATORS='["---","+++"]'
LANGGRAPH_SPLITTER_CHUNK_SIZE=200
LANGGRAPH_SPLITTER_CHUNK_OVERLAP=100

POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_USERNAME=postgres
POSTGRES_PASSWORD=password
POSTGRES_NAME=postgres

CHROMADB_HOST=chroma
CHROMADB_PORT=8000
```
2) Запустите
```bash
docker compose up -d
```

## Локальный запуск без Docker
1) Установите зависимости
```bash
pip install --upgrade pip
pip install -e .
```
2) Создайте `.env` (см. `env` как шаблон)
3) Запуск бота
```bash
python src/bot/main.py
```
4) Запуск API (FastAPI)
```bash
python src/application/main.py
# или
uvicorn src.application.main:run --factory --host 0.0.0.0 --port ${APP_API_PORT:-8080}
```

## Примечания
- Проект устанавливается как пакет, `PYTHONPATH` в Docker уже задан (`/app`). Локально это не требуется — импорты идут из `src/` (есть `src/__init__.py`).
- Стартовый документ кладите в папку `fixtures/` и укажите его имя в `APP_DEFAULT_DOC_FILE_PATH`.
- Первый запуск может занять время (скачивание моделей и зависимостей).



