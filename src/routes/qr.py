"""QR code generation and transmission routes"""

import logging
from flask import Blueprint, request, jsonify

from ..decorators import require_api_key
from ..services import send_qr_to_slack, get_bot_channels
from ..utils import bad_request, server_error, success_response

logger = logging.getLogger(__name__)

qr_bp = Blueprint('qr', __name__)


@qr_bp.route('/generate-qr', methods=['POST'])
@require_api_key
def generate_qr_webhook():
    """
    Generate QR code and send to Slack
    ---
    tags:
      - QR Code
    security:
      - ApiKeyAuth: []
    parameters:
      - name: body
        in: body
        required: true
        description: QR code generation request data
        schema:
          type: object
          required:
            - apk_url
            - channel
          properties:
            apk_url:
              type: string
              description: APK download URL
              example: "https://example.com/test-app.apk"
            channel:
              type: string
              description: Slack channel name (#channel-name) or channel ID (C0A4WE1RJNR)
              example: "#apk-qr-generator"
            build_number:
              type: string
              description: Build number (optional, displays 'latest' if not provided)
              example: "123"
    responses:
      200:
        description: QR code successfully sent to Slack
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: "QR code sent to Slack"
            file_id:
              type: string
              example: "F07KP4R8E9S"
      401:
        description: API 키 누락
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 401
            message:
              type: string
              example: "API key required"
            data:
              type: object
            payLoad:
              type: object
      403:
        description: 잘못된 API 키
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 403
            message:
              type: string
              example: "Invalid API key"
            data:
              type: object
            payLoad:
              type: object
      400:
        description: 필수 파라미터 누락
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Missing required parameters: apk_url, channel"
      500:
        description: 서버 오류
        schema:
          type: object
          properties:
            error:
              type: string
              example: "The request to the Slack API failed."
    """
    try:
        data = request.json
        
        # Check required parameters
        if not data or 'apk_url' not in data or 'channel' not in data:
            return jsonify(*bad_request("Missing required parameters: apk_url, channel"))
        
        apk_url = data['apk_url']
        channel = data['channel']
        build_number = data.get('build_number')
        
        # Generate and send QR code
        response = send_qr_to_slack(channel, apk_url, build_number)
        
        return jsonify({
            "success": True,
            "message": "QR code sent to Slack",
            "file_id": response['file']['id']
        }), 200
        
    except Exception as e:
        logger.error(f"Error in webhook: {str(e)}")
        return jsonify({"error": str(e)}), 500


@qr_bp.route('/generate-qr/broadcast', methods=['POST'])
@require_api_key
def broadcast_qr():
    """
    Send QR code to multiple channels
    ---
    tags:
      - QR Code
    security:
      - ApiKeyAuth: []
    parameters:
      - name: body
        in: body
        required: true
        description: Multi-channel QR transmission request
        schema:
          type: object
          required:
            - apk_url
            - channels
          properties:
            apk_url:
              type: string
              description: APK 다운로드 URL
              example: "https://example.com/test-app.apk"
            channels:
              type: array
              description: List of Slack channel names or IDs
              items:
                type: string
              example: ["#channel1", "#channel2", "C0A4WE1RJNR"]
            build_number:
              type: string
              description: Build number
              example: "123"
    responses:
      200:
        description: Successfully sent to all channels
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 200
            message:
              type: string
              example: "QR codes sent to all channels"
            data:
              type: object
              properties:
                success_count:
                  type: integer
                  example: 2
                failed_count:
                  type: integer
                  example: 0
                results:
                  type: array
                  items:
                    type: object
                    properties:
                      channel:
                        type: string
                        example: "#apk-qr-generator"
                      status:
                        type: string
                        example: "success"
                      file_id:
                        type: string
                        example: "F07KP4R8E9S"
                      error:
                        type: string
                        example: "Channel not found"
            payLoad:
              type: object
      401:
        description: API 키 누락
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 401
            message:
              type: string
              example: "API key required"
            data:
              type: object
            payLoad:
              type: object
      403:
        description: 잘못된 API 키
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 403
            message:
              type: string
              example: "Invalid API key"
            data:
              type: object
            payLoad:
              type: object
      400:
        description: 필수 파라미터 누락
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 400
            message:
              type: string
              example: "Missing required parameters: apk_url, channels"
            data:
              type: object
            payLoad:
              type: object
      500:
        description: 서버 오류
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 500
            message:
              type: string
              example: "The request to the Slack API failed."
            data:
              type: object
            payLoad:
              type: object
    """
    try:
        data = request.json
        
        if not data or 'apk_url' not in data or 'channels' not in data:
            return jsonify(*bad_request("Missing required parameters: apk_url, channels"))
        
        apk_url = data['apk_url']
        channels = data['channels']
        build_number = data.get('build_number')
        
        if not isinstance(channels, list) or len(channels) == 0:
            return jsonify(*bad_request("channels must be a non-empty array"))
        
        results = []
        success_count = 0
        failed_count = 0
        
        for channel in channels:
            try:
                response = send_qr_to_slack(channel, apk_url, build_number)
                results.append({
                    "channel": channel,
                    "status": "success",
                    "file_id": response['file']['id']
                })
                success_count += 1
            except Exception as e:
                results.append({
                    "channel": channel,
                    "status": "failed",
                    "error": str(e)
                })
                failed_count += 1
        
        return jsonify(*success_response(
            f"Sent to {success_count}/{len(channels)} channels",
            data={
                "success_count": success_count,
                "failed_count": failed_count,
                "results": results
            }
        ))
        
    except Exception as e:
        logger.error(f"Error in broadcast: {str(e)}")
        return jsonify(*server_error(str(e)))


@qr_bp.route('/generate-qr/custom', methods=['POST'])
@require_api_key
def generate_custom_qr():
    """
    Generate customizable QR code
    ---
    tags:
      - QR Code
    security:
      - ApiKeyAuth: []
    parameters:
      - name: body
        in: body
        required: true
        description: Custom QR code generation request
        schema:
          type: object
          required:
            - apk_url
            - channel
          properties:
            apk_url:
              type: string
              description: APK 다운로드 URL
              example: "https://example.com/test-app.apk"
            channel:
              type: string
              description: Slack channel name or ID
              example: "#apk-qr-generator"
            build_number:
              type: string
              description: 빌드 번호
              example: "123"
            qr_options:
              type: object
              description: QR code customization options
              properties:
                box_size:
                  type: integer
                  description: QR code box size
                  example: 15
                border:
                  type: integer
                  description: QR code border size
                  example: 4
                fill_color:
                  type: string
                  description: QR code color
                  example: "#000000"
                back_color:
                  type: string
                  description: Background color
                  example: "#FFFFFF"
    responses:
      200:
        description: Custom QR code sent successfully
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 200
            message:
              type: string
              example: "Custom QR code sent to Slack"
            data:
              type: object
              properties:
                file_id:
                  type: string
                  example: "F07KP4R8E9S"
            payLoad:
              type: object
      401:
        description: API 키 누락
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 401
            message:
              type: string
              example: "API key required"
            data:
              type: object
            payLoad:
              type: object
      403:
        description: 잘못된 API 키
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 403
            message:
              type: string
              example: "Invalid API key"
            data:
              type: object
            payLoad:
              type: object
      400:
        description: 필수 파라미터 누락
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 400
            message:
              type: string
              example: "Missing required parameters: apk_url, channel"
            data:
              type: object
            payLoad:
              type: object
      500:
        description: 서버 오류
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 500
            message:
              type: string
              example: "The request to the Slack API failed."
            data:
              type: object
            payLoad:
              type: object
    """
    try:
        data = request.json
        
        if not data or 'apk_url' not in data or 'channel' not in data:
            return jsonify(*bad_request("Missing required parameters: apk_url, channel"))
        
        apk_url = data['apk_url']
        channel = data['channel']
        build_number = data.get('build_number')
        qr_options = data.get('qr_options')
        
        # Generate and send QR code
        response = send_qr_to_slack(channel, apk_url, build_number, qr_options)
        
        return jsonify(*success_response(
            "Custom QR code sent to Slack",
            data={"file_id": response['file']['id']}
        ))
        
    except Exception as e:
        logger.error(f"Error in custom QR: {str(e)}")
        return jsonify(*server_error(str(e)))


@qr_bp.route('/generate-qr/broadcast-all', methods=['POST'])
@require_api_key
def broadcast_all_channels():
    """
    Send QR code to all channels the bot belongs to
    ---
    tags:
      - QR Code
    security:
      - ApiKeyAuth: []
    parameters:
      - name: body
        in: body
        required: true
        description: All channels QR transmission request
        schema:
          type: object
          required:
            - apk_url
          properties:
            apk_url:
              type: string
              description: APK 다운로드 URL
              example: "https://example.com/test-app.apk"
            build_number:
              type: string
              description: 빌드 번호
              example: "123"
            qr_options:
              type: object
              description: QR 코드 커스터마이징 옵션
              properties:
                box_size:
                  type: integer
                  example: 15
                border:
                  type: integer
                  example: 4
                fill_color:
                  type: string
                  example: "#000000"
                back_color:
                  type: string
                  example: "#FFFFFF"
    responses:
      200:
        description: Sent to all channels
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 200
            message:
              type: string
              example: "Sent to 3/5 channels"
            data:
              type: object
              properties:
                total_channels:
                  type: integer
                  example: 5
                success_count:
                  type: integer
                  example: 3
                failed_count:
                  type: integer
                  example: 2
                results:
                  type: array
                  items:
                    type: object
                    properties:
                      channel_id:
                        type: string
                      channel_name:
                        type: string
                      status:
                        type: string
                      file_id:
                        type: string
                      error:
                        type: string
            payLoad:
              type: object
      401:
        description: API 키 누락
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 401
            message:
              type: string
              example: "API key required"
            data:
              type: object
            payLoad:
              type: object
      403:
        description: 잘못된 API 키
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 403
            message:
              type: string
              example: "Invalid API key"
            data:
              type: object
            payLoad:
              type: object
      400:
        description: 필수 파라미터 누락
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 400
            message:
              type: string
              example: "Missing required parameter: apk_url"
            data:
              type: object
            payLoad:
              type: object
      500:
        description: 서버 오류
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 500
            message:
              type: string
              example: "Failed to retrieve channels"
            data:
              type: object
            payLoad:
              type: object
    """
    try:
        data = request.json
        
        if not data or 'apk_url' not in data:
            return jsonify(*bad_request("Missing required parameter: apk_url"))
        
        apk_url = data['apk_url']
        build_number = data.get('build_number')
        qr_options = data.get('qr_options')
        
        # Query all channels the bot belongs to
        try:
            all_channels = get_bot_channels()
        except Exception as e:
            logger.error(f"Failed to get channels: {str(e)}")
            return jsonify(*server_error(f"Failed to retrieve channels: {str(e)}"))
        
        if not all_channels:
            return jsonify(*bad_request("Bot is not a member of any channels"))
        
        # Send to all channels
        results = []
        success_count = 0
        failed_count = 0
        
        for channel in all_channels:
            channel_id = channel['id']
            channel_name = channel['name']
            
            try:
                response = send_qr_to_slack(channel_id, apk_url, build_number, qr_options)
                results.append({
                    "channel_id": channel_id,
                    "channel_name": channel_name,
                    "status": "success",
                    "file_id": response['file']['id']
                })
                success_count += 1
            except Exception as e:
                results.append({
                    "channel_id": channel_id,
                    "channel_name": channel_name,
                    "status": "failed",
                    "error": str(e)
                })
                failed_count += 1
        
        return jsonify(*success_response(
            f"Sent to {success_count}/{len(all_channels)} channels",
            data={
                "total_channels": len(all_channels),
                "success_count": success_count,
                "failed_count": failed_count,
                "results": results
            }
        ))
        
    except Exception as e:
        logger.error(f"Error in broadcast-all: {str(e)}")
        return jsonify(*server_error(str(e)))


# Apply rate limiting after blueprint registration
def apply_rate_limits(limiter):
    """Apply rate limiting to each endpoint"""
    limiter.limit("20 per minute")(generate_qr_webhook)
    limiter.limit("10 per minute")(broadcast_qr)
    limiter.limit("20 per minute")(generate_custom_qr)
    limiter.limit("5 per minute")(broadcast_all_channels)  # Lower limit for broadcast-all
