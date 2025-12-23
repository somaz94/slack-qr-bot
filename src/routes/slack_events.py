"""Slack Events API routes"""

import logging
from flask import Blueprint, request, jsonify

from ..services import send_qr_to_slack

logger = logging.getLogger(__name__)

slack_events_bp = Blueprint('slack_events', __name__)


@slack_events_bp.route('/slack/events', methods=['POST'])
def slack_events():
    """Slack Events API endpoint"""
    data = request.json
    
    # URL verification challenge response
    if 'challenge' in data:
        return jsonify({"challenge": data['challenge']})
    
    # Process events
    if 'event' in data:
        event = data['event']
        
        # Process message events
        if event['type'] == 'message' and 'apk_build' in event.get('text', ''):
            try:
                # Extract URL from message
                text = event['text']
                if 'URL:' in text:
                    apk_url = text.split('URL:')[1].strip()
                    channel = event['channel']
                    
                    # Generate and send QR
                    send_qr_to_slack(channel, apk_url)
                    
            except Exception as e:
                logger.error(f"Error processing event: {str(e)}")
    
    return jsonify({"status": "ok"}), 200
