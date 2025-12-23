"""Flask decorators"""

import logging
from functools import wraps
from flask import request, jsonify
from flask_limiter.util import get_remote_address

from .config import API_KEY
from .utils import unauthorized, forbidden

logger = logging.getLogger(__name__)


def require_api_key(f):
    """
    API key authentication decorator
    
    Requires authentication only when API_KEY environment variable is set.
    Validates API key passed via X-API-Key header.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Skip authentication if API key is not set
        if not API_KEY:
            return f(*args, **kwargs)
        
        # Check API key in headers
        provided_key = request.headers.get('X-API-Key')
        
        if not provided_key:
            logger.warning("API call without API key", extra={
                "remote_addr": get_remote_address(),
                "endpoint": request.endpoint
            })
            return jsonify(*unauthorized("API key required"))
        
        if provided_key != API_KEY:
            logger.warning("API call with invalid API key", extra={
                "remote_addr": get_remote_address(),
                "endpoint": request.endpoint
            })
            return jsonify(*forbidden("Invalid API key"))
        
        return f(*args, **kwargs)
    return decorated_function
