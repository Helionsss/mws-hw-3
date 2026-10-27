# API-автотесты в Docker

Тесты с прошлой домашки по REST и GraphQL (pytest + requests), упакованные в Docker-образ. Тест запускается сам при старте контейнера, а GitHub Actions на каждый push собирает образ и прогоняет его.

## Что проверяется

- **REST** (`tests/test_posts_flow.py`) — создание поста, `PATCH` и чтение: HTTP-статусы, id, изменённый title и то, что остальные поля не тронуты.
- **Авторизация** (`tests/test_auth.py`) — логин, запрос с Bearer-токеном и негативные сценарии: без токена, с неверным токеном, с неверными логином и паролем.
- **GraphQL** (`tests/test_graphql.py`) — query hello и mutation CreatePerson: HTTP 200, data, поля ответа и отсутствие errors.

Обе песочницы публичные: REST — `playground.nileslabs.com/api/v1`, GraphQL — `graphql.postman-echo.com/graphql`. Адреса и учётные данные при необходимости переопределяются переменными окружения `REST_BASE_URL`, `GRAPHQL_URL`, `API_USERNAME`, `API_PASSWORD`, `API_TIMEOUT` — по умолчанию стоят демо-данные playground.

## Запуск в Docker

```bash
docker build -t api-test .
docker run --rm api-test
```

Тест стартует сам, логи видны в консоли. Если всё прошло — процесс завершается с кодом 0, если что-то упало — с ненулевым:

```bash
docker run --rm api-test; echo $?
```

Проверить, что падение действительно ломает запуск, можно на несуществующем адресе:

```bash
docker run --rm -e REST_BASE_URL=http://127.0.0.1:1 api-test; echo $?
```

## CI

Конфиг — [`.github/workflows/ci.yml`](.github/workflows/ci.yml). Workflow запускается на каждый `push`: забирает код из репозитория, собирает образ и запускает его. Если образ не собирается или тест падает, job и pipeline краснеют.

## Что внутри

- `api/` — HTTP-клиент и обёртки над REST и GraphQL
- `tests/` — сценарии
- `pytest.ini`
- `Dockerfile` и `.dockerignore`
- `postman/` — коллекция с GraphQL-подпиской из прошлой работы

Тесты и коллекция переехали из [прошлой работы](https://github.com/Helionsss/mws-hw-2).
