"""Health check routes"""

import logging
from flask import Blueprint, jsonify

from ..services import check_slack_connection
from ..utils import success_response, error_response

logger = logging.getLogger(__name__)

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint (detailed)
    ---
    tags:
      - Health
    responses:
      200:
        description: Service is operating normally
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 200
            message:
              type: string
              example: "Service is healthy"
            data:
              type: object
              properties:
                status:
                  type: string
                  example: "healthy"
                slack_connection:
                  type: object
                  properties:
                    connected:
                      type: boolean
                      example: true
                    team:
                      type: string
                      example: "My Workspace"
            payLoad:
              type: object
      503:
        description: Service degraded
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 503
            message:
              type: string
              example: "Service degraded - Slack connection failed"
            data:
              type: object
              properties:
                status:
                  type: string
                  example: "unhealthy"
                slack_connection:
                  type: object
                  properties:
                    connected:
                      type: boolean
                      example: false
                    error:
                      type: string
                      example: "invalid_auth"
            payLoad:
              type: object
    """
    slack_status = check_slack_connection()
    
    if slack_status['connected']:
        return jsonify(*success_response(
            "Service is healthy",
            data={
                "status": "healthy",
                "slack_connection": slack_status
            }
        ))
    else:
        return jsonify(*error_response(
            503,
            "Service degraded - Slack connection failed",
            data={
                "status": "unhealthy",
                "slack_connection": slack_status
            }
        ))
