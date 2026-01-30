# Imports
import json
import logging

log = logging.getLogger(__name__)

from modules.get_config import invalidate_cache

# File paths
config_file = 'config.json'

# Saves new alarm time to config file
def save_alarm_time(new_alarm_time, file_path=config_file):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        data['alarm_time'] = new_alarm_time

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        invalidate_cache()
        log.info("Saved new alarm time")
        return
    except Exception:
        log.exception("Failed to save alarm time")
        raise

# Saves new clockout time to config file
def save_clockout_time(new_clockout_time, file_path=config_file):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        data['clockout_time'] = new_clockout_time

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        invalidate_cache()
        log.info("Saved new clockout time")
        return
    except Exception:
        log.exception("Failed to save clockout time")
        raise

# Saves new alarm day update to config file
def save_alarm_days(update, file_path=config_file):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        data['alarm_days'] = update

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        invalidate_cache()
        log.info("Saved new alarm days")
        return
    except Exception:
        log.exception("Failed to save alarm days")
        raise

# Toggles light control setting in config file
def toggle_light_control(file_path=config_file, key='light_control'):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        data[key] = not data.get(key, False)

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

        invalidate_cache()
        log.info("Toggled light control setting")
        return
    except Exception:
        log.exception("Failed to toggle light control")
        raise