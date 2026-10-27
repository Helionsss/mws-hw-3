from api.config import GRAPHQL_URL
from api.http_client import HttpClient


class GraphQLApi(HttpClient):
    def __init__(self):
        super().__init__(GRAPHQL_URL, {"Content-Type": "application/json"})

    def execute(self, query, variables=None):
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        return self.post(json=payload)
