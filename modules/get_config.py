# Imports
import json
from datetime import date, timedelta

# File paths
config_file = 'config.json'

# Gets alarm and clockout times from the config file to send to the frontend
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

def get_last_required_day():
    #todo update to get the date of the last needed day
    return date.today() - timedelta(days=1)