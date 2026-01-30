from os.path import isfile
import json
import requests
import logging

log = logging.getLogger(__name__)

from modules.get_config import get_alarm_time


def keys_file_there():
    try:
        return isfile('keys.json')
    except Exception:
        log.exception("Failed to check if keys.json exists")
        return False

def _get_user_key(file_path="keys.json"):
    try:
        with open(file_path, 'r') as file:
            content = file.read().strip()
            data = json.loads(content)

        user_key = data.get('user_key')

        return user_key
    
    except Exception:
        log.exception("Failed to read user key from keys.json")
        return None

def _get_app_token(file_path="keys.json"):
    try:
        with open(file_path, 'r') as file:
            content = file.read().strip()
            data = json.loads(content)

        app_token = data.get('app_token')

        return app_token
    
    except Exception:
        log.exception("Failed to read app token from keys.json")
        return None

def send_notification(title="Clockout within 1 Hour"):
    try:
        requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": _get_app_token(),
                "user": _get_user_key(),
                "title": title,
                "message": f"Alarm set for {get_alarm_time()}."
            },
            timeout=10
        )
        log.info("Notification sent via Pushover.")
    except Exception:
        log.error("Failed to send notification via Pushover.")
