import pytest

from api.graphql_api import GraphQLApi
from api.rest_api import RestApi


@pytest.fixture(scope="session")
def rest_api():
    return RestApi()


@pytest.fixture(scope="session")
def graphql_api():
    return GraphQLApi()
