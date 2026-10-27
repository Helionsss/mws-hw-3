import pytest

from api.checks import assert_status, assert_true, json_body
from api.config import API_PASSWORD, API_USERNAME

INVALID_CREDENTIALS = [
    pytest.param(API_USERNAME, "wrong-password", id="wrong-password"),
    pytest.param("unknown-user", API_PASSWORD, id="unknown-user"),
]

INVALID_AUTH_HEADERS = [
    pytest.param({}, id="missing-token"),
    pytest.param({"Authorization": "Bearer invalid-token"}, id="invalid-token"),
    pytest.param({"Authorization": "Basic dXNlcjpwYXNz"}, id="wrong-auth-scheme"),
]


def test_login_token_identifies_the_same_user(rest_api):
    login_response = rest_api.login()
    assert_status(login_response, 200)
    login_body = json_body(login_response)
    token = login_body.get("access_token")
    assert_true(isinstance(token, str) and bool(token.strip()), "access_token must be a non-empty string", login_response)

    me_response = rest_api.get_me(token)
    assert_status(me_response, 200)
    profile = json_body(me_response)
    assert_true(profile.get("id") == login_body.get("user", {}).get("id"), "Profile id differs from login user id", me_response)
    assert_true(
        str(profile.get("username", "")).lower() == API_USERNAME.lower(),
        "Profile username differs from login username",
        me_response,
    )
    assert_true(bool(profile.get("email")), "Profile must contain an email", me_response)


@pytest.mark.parametrize("headers", INVALID_AUTH_HEADERS)
def test_profile_access_is_rejected_without_valid_token(rest_api, headers):
    response = rest_api.get_me_with_headers(headers)
    assert_true(response.status_code in (401, 403), f"Expected access denial, got {response.status_code}", response)
    body = json_body(response)
    assert_true(bool(body.get("error") or body.get("message")), "Access denial must explain the reason", response)


@pytest.mark.parametrize("username,password", INVALID_CREDENTIALS)
def test_login_rejects_invalid_credentials(rest_api, username, password):
    response = rest_api.login(username, password)
    assert_true(response.status_code in (400, 401), f"Expected login rejection, got {response.status_code}", response)
    body = json_body(response)
    assert_true(bool(body.get("error") or body.get("message")), "Login rejection must explain the reason", response)
