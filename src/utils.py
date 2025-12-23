"""Utility functions"""


def create_response(code, message, data=None, payload=None):
    """
    Create standard API response format
    
    Args:
        code: HTTP status code
        message: Response message
        data: Response data (default: {})
        payload: Additional payload (default: {})
    
    Returns:
        tuple: (response dictionary, HTTP status code)
    """
    return {
        "code": code,
        "message": message,
        "data": data if data is not None else {},
        "payLoad": payload if payload is not None else {}
    }, code


def success_response(message, data=None, payload=None):
    """200 success response"""
    return create_response(200, message, data, payload)


def error_response(code, message, data=None, payload=None):
    """Error response"""
    return create_response(code, message, data, payload)


def bad_request(message="Bad request", data=None):
    """400 Bad Request"""
    return error_response(400, message, data)


def unauthorized(message="Unauthorized", data=None):
    """401 Unauthorized"""
    return error_response(401, message, data)


def forbidden(message="Forbidden", data=None):
    """403 Forbidden"""
    return error_response(403, message, data)


def not_found(message="Not found", data=None):
    """404 Not Found"""
    return error_response(404, message, data)


def server_error(message="Internal server error", data=None):
    """500 Internal Server Error"""
    return error_response(500, message, data)
