from os.path import isfile
import json
import requests

from modules.get_config import get_alarm_time

def keys_file_there():
    return isfile('keys.json')

def get_user_key(file_path="keys.json"):
    with open(file_path, 'r') as file:
        content = file.read().strip()
        data = json.loads(content)

    user_key = data.get('user_key')

    return user_key

def get_app_token(file_path="keys.json"):
    with open(file_path, 'r') as file:
        content = file.read().strip()
        data = json.loads(content)

    app_token = data.get('app_token')

    return app_token

def send_notification(title="Clockout within 1 Hour"):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": get_app_token(),
            "user": get_user_key(),
            "title": title,
            "message": f"Alarm set for {get_alarm_time()}."
        },
        timeout=10
    )
