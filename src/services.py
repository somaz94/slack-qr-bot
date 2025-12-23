"""QR code generation and Slack transmission service"""

import os
import io
import logging
import qrcode
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

# Initialize Slack client
slack_token = os.environ.get("SLACK_BOT_TOKEN")
slack_client = WebClient(token=slack_token)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(SlackApiError),
    reraise=True
)
def check_slack_connection():
    """Check Slack API connection status (with retry logic)"""
    try:
        response = slack_client.auth_test()
        return {
            "connected": True,
            "team": response.get("team"),
            "user": response.get("user"),
            "bot_id": response.get("bot_id")
        }
    except SlackApiError as e:
        logger.error(f"Slack connection failed: {e.response['error']}")
        return {
            "connected": False,
            "error": e.response['error']
        }


def generate_qr_code(url, box_size=10, border=4, fill_color="black", back_color="white"):
    """Convert URL to QR code image (customizable)"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    
    # Convert image to bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return img_byte_arr


def get_channel_id(channel_name_or_id):
    """Convert channel name to channel ID"""
    # Return as-is if already in ID format (starts with C, G, D, Z and at least 9 characters)
    if channel_name_or_id.startswith(('C', 'G', 'D', 'Z')) and len(channel_name_or_id) >= 9:
        logger.info(f"Using channel ID directly: {channel_name_or_id}")
        return channel_name_or_id
    
    # Remove # prefix
    clean_name = channel_name_or_id.lstrip('#')
    logger.info(f"Looking up channel name: {clean_name}")
    
    try:
        # Query public and private channels
        cursor = None
        while True:
            response = slack_client.conversations_list(
                types="public_channel,private_channel",
                cursor=cursor,
                limit=200
            )
            
            for channel in response['channels']:
                if channel['name'] == clean_name:
                    logger.info(f"Found channel ID: {channel['id']} for name: {clean_name}")
                    return channel['id']
            
            cursor = response.get('response_metadata', {}).get('next_cursor')
            if not cursor:
                break
        
        raise ValueError(f"Channel not found: {clean_name}")
        
    except SlackApiError as e:
        logger.error(f"Error looking up channel: {e.response['error']}")
        raise


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(SlackApiError),
    reraise=True
)
def get_bot_channels():
    """Retrieve list of all channels the bot belongs to"""
    try:
        channels = []
        cursor = None
        
        while True:
            response = slack_client.conversations_list(
                types="public_channel,private_channel",
                cursor=cursor,
                limit=200
            )
            
            for channel in response['channels']:
                if channel.get('is_member', False):
                    channels.append({
                        "id": channel['id'],
                        "name": channel['name'],
                        "is_private": channel.get('is_private', False),
                        "num_members": channel.get('num_members', 0)
                    })
            
            cursor = response.get('response_metadata', {}).get('next_cursor')
            if not cursor:
                break
        
        return channels
        
    except SlackApiError as e:
        logger.error(f"Error fetching channels: {e.response['error']}")
        raise


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(SlackApiError),
    reraise=True
)
def send_qr_to_slack(channel, apk_url, build_number=None, qr_options=None):
    """Generate QR code and send to Slack channel"""
    try:
        # Convert channel name to ID
        channel_id = get_channel_id(channel)
        
        # Check channel access (for debugging - continue even if it fails)
        try:
            channel_info = slack_client.conversations_info(channel=channel_id)
            logger.info(f"Channel info: {channel_info['channel']['name']}")
            logger.info(f"Channel is_private: {channel_info['channel'].get('is_private', False)}")
            logger.info(f"Channel is_member: {channel_info['channel'].get('is_member', False)}")
        except SlackApiError as e:
            logger.warning(f"Cannot get channel info (will try upload anyway): {e.response['error']}")
        
        # Generate QR code (apply custom options)
        if qr_options:
            qr_image = generate_qr_code(
                apk_url,
                box_size=qr_options.get('box_size', 10),
                border=qr_options.get('border', 4),
                fill_color=qr_options.get('fill_color', 'black'),
                back_color=qr_options.get('back_color', 'white')
            )
        else:
            qr_image = generate_qr_code(apk_url)
        
        # Compose message
        message = f"📱 *Android APK Build Complete!*\n\n"
        if build_number:
            message += f"Build Number: #{build_number}\n"
        message += f"APK URL: {apk_url}\n\n"
        message += "👇 Scan QR code to download"
        
        # Upload file to Slack
        response = slack_client.files_upload_v2(
            channel=channel_id,
            file=qr_image,
            filename=f"apk-qrcode-{build_number or 'latest'}.png",
            initial_comment=message
        )
        
        logger.info(f"QR code sent successfully to {channel_id}")
        return response
        
    except SlackApiError as e:
        logger.error(f"Error sending QR code: {e.response['error']}")
        logger.error(f"Channel: {channel}")
        logger.error(f"Full error response: {e.response}")
        raise
    except ValueError as e:
        logger.error(f"Channel lookup error: {str(e)}")
        raise
