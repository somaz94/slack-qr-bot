"""Tests for utility functions"""

from src.utils import (
    create_response,
    success_response,
    error_response,
    bad_request,
    unauthorized,
    forbidden,
    not_found,
    server_error,
)


class TestCreateResponse:
    def test_basic_response(self):
        body, code = create_response(200, "OK")
        assert code == 200
        assert body["code"] == 200
        assert body["message"] == "OK"
        assert body["data"] == {}
        assert body["payLoad"] == {}

    def test_response_with_data(self):
        body, code = create_response(200, "OK", data={"key": "value"})
        assert body["data"] == {"key": "value"}

    def test_response_with_payload(self):
        body, code = create_response(200, "OK", payload={"extra": True})
        assert body["payLoad"] == {"extra": True}


class TestSuccessResponse:
    def test_default(self):
        body, code = success_response("Done")
        assert code == 200
        assert body["message"] == "Done"

    def test_with_data(self):
        body, code = success_response("Done", data={"id": 1})
        assert body["data"] == {"id": 1}


class TestErrorResponses:
    def test_error_response(self):
        body, code = error_response(422, "Validation error")
        assert code == 422
        assert body["message"] == "Validation error"

    def test_bad_request(self):
        body, code = bad_request()
        assert code == 400
        assert body["message"] == "Bad request"

    def test_bad_request_custom(self):
        body, code = bad_request("Missing field")
        assert body["message"] == "Missing field"

    def test_unauthorized(self):
        body, code = unauthorized()
        assert code == 401

    def test_forbidden(self):
        body, code = forbidden()
        assert code == 403

    def test_not_found(self):
        body, code = not_found()
        assert code == 404

    def test_server_error(self):
        body, code = server_error()
        assert code == 500
