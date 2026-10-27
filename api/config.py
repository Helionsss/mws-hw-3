import os

REST_BASE_URL = os.getenv("REST_BASE_URL", "https://playground.nileslabs.com/api/v1")
GRAPHQL_URL = os.getenv("GRAPHQL_URL", "https://graphql.postman-echo.com/graphql")
API_USERNAME = os.getenv("API_USERNAME", "Bret")
API_PASSWORD = os.getenv("API_PASSWORD", "Password@123")
REQUEST_TIMEOUT = float(os.getenv("API_TIMEOUT", "30"))
DEFAULT_USER_ID = 1
DEFAULT_HEADERS = {
    "Accept": "application/json",
    "User-Agent": "PostmanRuntime/7.39.0",
}
