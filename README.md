# trello-api-tests

Производственный API-автотестовый фреймворк для **Trello REST API**.  
Первый проект дипломной экосистемы QA: **API-first** — сущности создаются через API и переиспользуются в `trello_ui` и `trello_mobile`.

Связанные репозитории: **trello_ui**, **trello_mobile** (API-first). CI и Allure TestOps — см. `docs/CI.md`.

## Обзор проекта

| Аспект | Описание |
|--------|----------|
| Домен | Trello API v1 |
| Роль в экосистеме | Data Provider для UI/Mobile тестов |
| Подход | API создаёт ресурсы → UI/Mobile проверяют отображение |
| Уровень | Enterprise-архитектура автоматизации |

## Стек

- Python 3.14+
- [Pytest](https://docs.pytest.org/) — раннер и фикстуры
- [Requests](https://requests.readthedocs.io/) — HTTP-клиент
- [Pydantic v2](https://docs.pydantic.dev/) — типизированные request/response модели
- [Allure](https://docs.qameta.io/allure/) — отчётность
- [python-dotenv](https://github.com/theskumar/python-dotenv) — конфигурация
- [Faker](https://faker.readthedocs.io/) — генерация данных
- Logging — структурированные логи запросов/ответов
- GitHub Actions — CI

## Архитектура

```
┌─────────────────────────────────────────────────────────────┐
│                      tests/ (Pytest)                        │
│   test_auth · test_boards · test_lists · test_cards · ...   │
└──────────────────────────┬──────────────────────────────────┘
                           │ фикстуры / assertions
┌──────────────────────────▼──────────────────────────────────┐
│                    fixtures/ + conftest.py                    │
│   prepare_board · prepare_list · prepare_card · EntityContext │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                      api/client.py                          │
│         Единая точка HTTP (Allure steps + logging)          │
└───────┬──────────────────────────────────────┬──────────────┘
        │                                      │
┌───────▼────────┐                    ┌──────▼───────┐
│ models/request │                    │models/response│
│   Pydantic v2  │                    │  Pydantic v2  │
└────────────────┘                    └──────────────┘
        │                                      │
┌───────▼──────────────────────────────────────▼──────────────┐
│              utils/ (config · logger · attach)               │
└──────────────────────────┬──────────────────────────────────┘
                           │
                    Trello REST API
```

### Слои

| Слой | Назначение |
|------|------------|
| `tests/` | Тонкие сценарии, только бизнес-шаги и проверки |
| `api/client.py` | Все HTTP-вызовы, без `requests` в тестах |
| `api/endpoints.py` | Константы путей — без magic strings |
| `api/assertions.py` | Переиспользуемые проверки |
| `api/helpers.py` | Парсинг и валидация ответов |
| `models/` | Контракты запросов и ответов |
| `fixtures/generators.py` | Фабрики сущностей + `EntityContext` для UI/Mobile |
| `utils/` | Конфиг, логи, Allure-вложения |

### Интеграция API → UI → Mobile

`EntityContext.as_dict()` возвращает идентификаторы созданных сущностей (`board_id`, `list_id`, `card_id`, …) — их можно экспортировать в JSON/переменные окружения для последующих репозиториев.

## Структура репозитория

```
trello-api-tests/
├── .github/workflows/api-tests.yml
├── api/
│   ├── client.py
│   ├── endpoints.py
│   ├── assertions.py
│   └── helpers.py
├── models/
│   ├── request/
│   │   ├── create_board.py
│   │   ├── create_list.py
│   │   ├── create_card.py
│   │   └── update_card.py
│   └── response/
│       ├── board_response.py
│       ├── list_response.py
│       ├── card_response.py
│       └── member_response.py
├── fixtures/
│   ├── generators.py
│   └── test_data.py
├── utils/
│   ├── config.py
│   ├── logger.py
│   └── attach.py
├── tests/
│   ├── test_auth.py
│   ├── test_boards.py
│   ├── test_lists.py
│   ├── test_cards.py
│   ├── test_checklists.py
│   └── test_members.py
├── .env.example
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## Установка

```bash
git clone <url-репозитория>
cd trello_api
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Конфигурация

1. Скопируйте `.env.example` в `.env`:
   ```bash
   copy .env.example .env   # Windows
   cp .env.example .env     # Linux/macOS
   ```

2. Получите ключ и токен:
   - [Trello Developer API Keys](https://trello.com/app-key)
   - Сгенерируйте Token (ссылка на странице ключа)

3. Заполните `.env`:

```env
TRELLO_BASE_URL=https://api.trello.com/1
TRELLO_API_KEY=ваш_api_key
TRELLO_API_TOKEN=ваш_api_token
```

## Запуск тестов

```bash
# все тесты
pytest

# подробный вывод
pytest -v

# по маркерам
pytest -m smoke
pytest -m boards

# один файл
pytest tests/test_cards.py
```

### Данные для UI (Selenium)

Создать доску, список, карточку, чек-лист → проверить через API → сохранить `artifacts/test-context.json` (сущности **не удаляются**):

```bash
pytest -m ui_setup
# или
python scripts/provision_ui_data.py
```

Удалить созданные ресурсы и файл контекста:

```bash
pytest -m ui_teardown
# или
python scripts/cleanup_ui_data.py
```

В JSON — `board_url`, `card_name`, `list_name` и id для репозитория `trello_ui`.
Повторный `ui_setup` сначала удалит доску из предыдущего контекста (если файл ещё есть).
```

## Allure-отчёт

```bash
# установите Allure CLI: https://docs.qameta.io/allure/#_installing_a_commandline
pytest --alluredir=allure-results
allure serve allure-results
```

В отчёте: feature/story/title, шаги, payload запроса, тело ответа, status code.

## CI (GitHub Actions)

Workflow: `.github/workflows/api-tests.yml`

**Secrets в репозитории:**

| Secret | Описание |
|--------|----------|
| `TRELLO_BASE_URL` | Базовый URL API |
| `TRELLO_API_KEY` | API Key |
| `TRELLO_API_TOKEN` | API Token |

Артефакт `allure-results` загружается после каждого прогона.

## Покрытие тестов

| Модуль | Тесты |
|--------|-------|
| Auth | `test_get_current_user`, `test_invalid_token` |
| Boards | create, get, update, delete, без имени |
| Lists | create, get, rename |
| Cards | create, get, update desc, move, archive, delete |
| Checklists | create checklist, add checkitem |
| Members | boards, workspaces |

## Принципы качества

- PEP 8, типизация, SOLID на уровне слоёв
- DRY: фикстуры и generators вместо дублирования setup
- Без magic strings: `Endpoints`, константы в `test_data.py`
- Негативные сценарии через `raw_request(validate=False)`

## Лицензия

Учебный проект дипломной программы QA.
