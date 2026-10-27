from api.config import API_PASSWORD, API_USERNAME, DEFAULT_USER_ID, REST_BASE_URL
from api.http_client import HttpClient


class RestApi(HttpClient):
    def __init__(self):
        super().__init__(REST_BASE_URL)

    def create_post(self, title, body, user_id=DEFAULT_USER_ID):
        return self.post("/posts", json={"title": title, "body": body, "user_id": user_id})

    def patch_post(self, post_id, **fields):
        return self.patch(f"/posts/{post_id}", json=fields)

    def get_post(self, post_id):
        return self.get(f"/posts/{post_id}")

    def login(self, username=API_USERNAME, password=API_PASSWORD):
        return self.post("/auth/login", json={"username": username, "password": password})

    def get_me(self, token=None):
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        return self.get_me_with_headers(headers)

    def get_me_with_headers(self, headers):
        return self.get("/auth/me", headers=headers)
