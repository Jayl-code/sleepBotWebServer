# Module: get_config.py

# Imports
import json
from datetime import date, timedelta, datetime
import os
import logging

log = logging.getLogger(__name__)

# File paths
config_file = 'config.json'

# Cache variables
_config_cache = None
_config_mtime = None

# Index mapping for days of the week
day_index = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6
    }

# Load config from file and cache it. Reload if file has changed.
def _load_config():
    global _config_cache, _config_mtime
    
    try:
        # Check if file has been modified
        current_mtime = os.path.getmtime(config_file) # Get time of last modification
        if _config_cache is not None and current_mtime == _config_mtime:
            return _config_cache  # Use cache
        
        # File changed or first load - read it
        with open(config_file, 'r') as file:
            _config_cache = json.load(file)
            _config_mtime = current_mtime
            return _config_cache
    except Exception:
        log.exception("Failed to load config file")
        raise

# Gets alarm and clockout times
def get_alarm_time():
    config = _load_config()
    return config.get('alarm_time')

def get_clockout_time():
    config = _load_config()
    return config.get('clockout_time')

# Convert day name into date of its last day (Helper function)
def _get_date_of_last_day(target_day_name):
    target = day_index[target_day_name.lower()]
    today = date.today().weekday()  # number 0–6
    days_back = (today - target) % 7 or 7 # Wrap around to previous week
    return date.today() - timedelta(days=days_back)

# Find the most recent day before today that has alarm active and return its date
def get_last_required_day(): 
    config = _load_config()
    
    #Get today's day name
    todays_day = datetime.today().strftime("%A").lower()
    idx = day_index[todays_day]
    checking_index = (idx - 1) % 7
    
    index_to_weekday = {v: k for k, v in day_index.items()}

    # Loop through days backwards to find last active day
    for _ in range(7):
        checking_day_name = index_to_weekday[checking_index]

        if config["alarm_days"][checking_day_name] == True:
            return _get_date_of_last_day(checking_day_name)
        
        # Check previous day in next iteration
        checking_index = (checking_index - 1) % 7

    return None  # No active days found

# Returns True if alarm is active today, otherwise False
def alarm_today():
    config = _load_config()
    # Get today's day name
    todays_day = datetime.today().strftime("%A").lower()
    return config["alarm_days"][todays_day]

# Returns alarm days dictionary from config file
def get_alarm_days():
    config = _load_config()
    return config.get('alarm_days')

# Returns True if light control is enabled, otherwise False
def get_is_light_control_enabled():
    config = _load_config()
    return config.get('light_control', False)

# Call this after writing config to refresh cache
def invalidate_cache():
    global _config_cache, _config_mtime
    _config_cache = None
    _config_mtime = None