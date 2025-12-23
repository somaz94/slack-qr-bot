"""Channel list retrieval routes"""

import logging
from flask import Blueprint, jsonify

from ..services import get_bot_channels
from ..utils import success_response, server_error

logger = logging.getLogger(__name__)

channels_bp = Blueprint('channels', __name__)


@channels_bp.route('/channels', methods=['GET'])
def list_channels():
    """
    Retrieve list of channels the bot belongs to
    ---
    tags:
      - Channels
    responses:
      200:
        description: Channel list
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 200
            message:
              type: string
              example: "Channels retrieved successfully"
            data:
              type: object
              properties:
                channels:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: string
                        example: "C0A4WE1RJNR"
                      name:
                        type: string
                        example: "apk-qr-generator"
                      is_private:
                        type: boolean
                        example: false
                      num_members:
                        type: integer
                        example: 5
                count:
                  type: integer
                  example: 3
            payLoad:
              type: object
      500:
        description: Server error
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 500
            message:
              type: string
              example: "Failed to fetch channels"
            data:
              type: object
            payLoad:
              type: object
    """
    try:
        channels = get_bot_channels()
        return jsonify(*success_response(
            "Channels retrieved successfully",
            data={
                "channels": channels,
                "count": len(channels)
            }
        ))
    except Exception as e:
        logger.error(f"Error fetching channels: {str(e)}")
        return jsonify(*server_error("Failed to fetch channels"))
