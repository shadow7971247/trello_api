# CI: Jenkins + Allure TestOps

Репозиторий **trello_api** — первая стадия пайплайна (API-first).

## Jenkins (этот репозиторий)

```bash
pip install -r requirements.txt
pytest -m "not browserstack" --alluredir=allure-results
# или только smoke:
pytest -m smoke --alluredir=allure-results
```

Секреты: `TRELLO_API_KEY`, `TRELLO_API_TOKEN`, `TRELLO_EMAIL`, `TRELLO_PASSWORD`.

## Экосистема

| Репозиторий | Роль |
|-------------|------|
| trello_api | API-тесты, клиент для UI/Mobile |
| trello_ui | Selenium; нужен клон **trello_api** рядом или `TRELLO_API_PATH` |
| trello_mobile | Appium; LambdaTest — `pytest -m lambdatest_smoke --run-context lambdatest` |

## Allure TestOps

```bash
allurectl upload --endpoint %ALLURE_ENDPOINT% ^
  --token %ALLURE_TOKEN% ^
  --project-id %ALLURE_PROJECT_ID% ^
  --launch-name "trello-api-%BUILD_NUMBER%" ^
  allure-results
```
