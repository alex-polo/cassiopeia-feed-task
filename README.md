# cassiopeia-feed-task

## Требования

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (опционально, рекомендуется)

## Описание

```bash
cassiopeia-feed-task/
├── pyproject.toml # Конфигурация проекта
├── README.md # Документация
├── run.py # Точка входа для ручного запуска
├── yml_catalog.xml # Сгенерированный YML-фид (после запуска run.py)
├── src/
│ └── feed/
│ ├── init.py
│ ├── constants.py # BASE_URL, COMPANY, COMPANY_NAME
│ ├── data.py # CATEGORIES, PRODUCTS (тестовые данные)
│ ├── feed_task.py # build_yml() - оркестратор
│ ├── utils.py # Валидация, парсинг, форматирование
│ ├── xml_builder.py # Генерация XML через ElementTree
│ └── views.py # Django view (пример интеграции)
└── tests/
├── conftest.py # Фикстуры pytest
├── test_integration.py # Интеграционные тесты
└── test_utils.py # Юнит-тесты для utils.py
```

## Установка

### Способ 1: Через uv (рекомендуется)

```bash
# Клонировать репозиторий
cd cassiopeia-feed-task

# Установить зависимости
uv sync
```

### Способ 2: Через pip

```bash
# Клонировать репозиторий
cd cassiopeia-feed-task

# Создать виртуальное окружение
python -m venv .venv

# Активировать
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Установить зависимости
pip install django django-stubs mypy pytest pytest-cov pytest-deadfixtures pytest-html ruff
```

## Запуск

```bash
# Через uv
uv run run.py

# Через python
python run.py
```

Сгенерирует yml_catalog.xml в корне проекта и выведет содержимое в консоль.

## Тестирование

```bash
# Через uv
uv run pytest

# Через python
pytest
```

## Проверка качества кода

```bash
# Типизация (mypy strict mode)
uv run mypy
# или
mypy

# Линтер (ruff)
uv run ruff check .
# или
ruff check .

# Форматирование
uv run ruff format .
# или
ruff format .
```
