# Imports
import json
from datetime import date, timedelta, datetime

# File paths
config_file = 'config.json'

day_index = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6
    }

# Gets alarm and clockout times from the config file
def get_alarm_time(file_path=config_file):
    with open(file_path, 'r') as file:
        content = file.read().strip()
        data = json.loads(content)

    alarm_time = data.get('alarm_time')
    
    return alarm_time

def get_clockout_time(file_path=config_file):
    with open(file_path, 'r') as file:
        content = file.read().strip()
        data = json.loads(content)

    clockout_time = data.get('clockout_time')
    
    return clockout_time

# Convert day name into date of its last day
def get_date_of_last_day(target_day_name):
    target = day_index[target_day_name.lower()]
    today = date.today().weekday()  # number 0–6
    days_back = (today - target) % 7 or 7
    return date.today() - timedelta(days=days_back)

def get_last_required_day(file_path=config_file):
    todays_day =  datetime.today().strftime("%A").lower()
    idx = day_index[todays_day]
    checking_index = (idx - 1) % 7

    index_to_weekday = {v: k for k, v in day_index.items()}

    with open(file_path, 'r') as file:
        content = file.read().strip()
        data = json.loads(content)

    for i in range(7):
        checking_day_name = index_to_weekday[checking_index]
        if data["alarm_days"][checking_day_name] == True:
            return get_date_of_last_day(checking_day_name)
        checking_index = (checking_index - 1) % 7

    return 

def alarm_today(file_path=config_file):
    todays_day =  datetime.today().strftime("%A").lower()

    with open(file_path, 'r') as file:
        content = file.read().strip()
        data = json.loads(content)
    
    active_today = data["alarm_days"][todays_day]

    return active_today

def get_alarm_days(file_path=config_file):
    with open(file_path, 'r') as file:
        content = file.read().strip()
        data = json.loads(content)

    alarm_data = data.get('alarm_days')
    
    return alarm_data

def get_is_light_control_enabled(file_path=config_file):
    with open(file_path, 'r') as file:
        content = file.read().strip()
        data = json.loads(content)

    light_control = data.get('light_control')
    
    return light_control