from uuid import uuid4

from api.checks import assert_status, assert_true, json_body


def test_create_patch_get_post_keeps_id_and_untouched_fields(rest_api):
    original_title = f"autotest post {uuid4()}"
    original_body = f"autotest body {uuid4()}"
    patched_title = f"{original_title} (patched)"

    created_response = rest_api.create_post(original_title, original_body)
    assert_status(created_response, 201)
    created_post = json_body(created_response)
    post_id = created_post.get("id")
    assert_true(bool(post_id), "Created post must return a non-empty id", created_response)
    assert_true(created_post.get("title") == original_title, "Created post title mismatch", created_response)

    patched_response = rest_api.patch_post(post_id, title=patched_title)
    assert_status(patched_response, 200)
    assert_true(json_body(patched_response).get("title") == patched_title, "PATCH did not change title", patched_response)

    fetched_response = rest_api.get_post(post_id)
    assert_status(fetched_response, 200)
    fetched_post = json_body(fetched_response)
    assert_true(fetched_post.get("id") == post_id, "GET post id does not match created id", fetched_response)
    assert_true(fetched_post.get("title") == patched_title, "PATCHed title was not persisted", fetched_response)
    assert_true(fetched_post.get("body") == original_body, "Body changed although PATCH touched only title", fetched_response)
