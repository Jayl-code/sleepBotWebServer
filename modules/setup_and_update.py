# Imports
import json
import sqlite3

# File paths
config_file = 'config.json'
db_file = 'database.db'

# Sends config data (alarm time, clockout time) to frontend and sets defaults if config file is empty
def get_config(file_path=config_file):
    defaults = {
    "alarm_time": "00:00",
    "clockout_time": "00:00",
    "alarm_days": {
        "monday": True,
        "tuesday": True,
        "wednesday": True,
        "thursday": True,
        "friday": True,
        "saturday": True,
        "sunday": True
    },
    "clockout_days": {
        "monday": True,
        "tuesday": True,
        "wednesday": True,
        "thursday": True,
        "friday": True,
        "saturday": True,
        "sunday": True
    }
}
    with open(file_path, 'r') as file:
        content = file.read().strip()
        if not content:  # empty file
            data = {}
        else:
            data = json.loads(content)

    if not data:
        with open(file_path, "w") as f:
            json.dump(defaults, f, indent=4)
        data = defaults
    
    alarm_time = data.get('alarm_time')
    clockout_time = data.get('clockout_time')
    
    return alarm_time, clockout_time

# Retrieves current streak, highscore, and score from the database to send to frontend
def get_update():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.execute("SELECT streak FROM history ORDER BY id DESC LIMIT 1")
    streak = cur.fetchone()

    cur.execute("SELECT score FROM history ORDER BY score DESC LIMIT 1")
    highscore = cur.fetchone()

    cur.execute("SELECT score FROM history ORDER BY id DESC LIMIT 1")
    score = cur.fetchone()
    
    cur.close()
    conn.close()
    if streak is None:
        return 0, 0, 0  # no data yet
    return streak[0], highscore[0], score[0]

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