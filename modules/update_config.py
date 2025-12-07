# Imports
import json

# File paths
config_file = 'config.json'

# Saves new alarm time to config file
def save_alarm_time(new_alarm_time, file_path=config_file):
    with open(file_path, 'r') as file:
        data = json.load(file)

    data['alarm_time'] = new_alarm_time

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return

# Saves new clockout time to config file
def save_clockout_time(new_clockout_time, file_path=config_file):
    with open(file_path, 'r') as file:
        data = json.load(file)

    data['clockout_time'] = new_clockout_time

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return

def save_alarm_days(update, file_path=config_file):
    with open(file_path, 'r') as file:
        data = json.load(file)

    data['alarm_days'] = update

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return