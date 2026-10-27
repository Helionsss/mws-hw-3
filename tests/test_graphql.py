from uuid import uuid4

from api.checks import assert_status, assert_true, json_body

HELLO_QUERY = "query { hello }"

CREATE_PERSON_MUTATION = """
mutation CreatePerson($person: PersonInput!) {
  createPerson(person: $person) {
    id
    name
    age
  }
}
"""

UNKNOWN_FIELD_QUERY = "query { fieldThatDoesNotExist }"


def test_hello_query_returns_data_without_errors(graphql_api):
    response = graphql_api.execute(HELLO_QUERY)
    assert_status(response, 200)
    payload = json_body(response)
    assert_true("errors" not in payload, "Successful query must not contain errors", response)
    assert_true(
        payload.get("data", {}).get("hello") == "Hello John Doe",
        "Query data must contain the expected hello greeting",
        response,
    )


def test_create_person_mutation_returns_created_person(graphql_api):
    person = {"name": f"Autotest Person {uuid4()}", "age": 30}

    response = graphql_api.execute(CREATE_PERSON_MUTATION, {"person": person})
    assert_status(response, 200)
    payload = json_body(response)
    assert_true("errors" not in payload, "Successful mutation must not contain errors", response)
    created_person = payload.get("data", {}).get("createPerson")
    assert_true(isinstance(created_person, dict), "Mutation data must contain createPerson", response)
    assert_true(bool(str(created_person.get("id", "")).strip()), "Created person must have an id", response)
    assert_true(created_person.get("name") == person["name"], "Created person name mismatch", response)
    assert_true(created_person.get("age") == person["age"], "Created person age mismatch", response)


def test_unknown_field_query_returns_graphql_errors(graphql_api):
    response = graphql_api.execute(UNKNOWN_FIELD_QUERY)
    assert_status(response, 200)
    payload = json_body(response)
    assert_true(bool(payload.get("errors")), "Unknown field must produce GraphQL errors", response)
