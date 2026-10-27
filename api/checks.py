def describe_response(response):
    request = response.request
    return (
        f"\nrequest: {request.method} {request.url}"
        f"\nrequest body: {request.body}"
        f"\nresponse status: {response.status_code}"
        f"\nresponse body: {response.text}"
    )


def assert_status(response, expected):
    assert response.status_code == expected, (
        f"Expected HTTP {expected}, got {response.status_code}{describe_response(response)}"
    )


def assert_true(condition, message, response):
    assert condition, f"{message}{describe_response(response)}"


def json_body(response):
    try:
        return response.json()
    except ValueError:
        raise AssertionError(f"Response is not valid JSON{describe_response(response)}")
