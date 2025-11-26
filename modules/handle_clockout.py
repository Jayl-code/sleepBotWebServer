# Imports
import json
from datetime import datetime, date, timedelta
import sqlite3

# File paths
config_file = 'config.json'
db_file = 'database.db'


# Processes clockout action and updates database accordingly
def clockout_action():
    date_of_alarm = None
    clockout_completed = None

    allowed_time_before_amount = 4 # Hours

    alarm_time, clockout_time = get_config()

    alarm_time = datetime.strptime(alarm_time, "%H:%M").time()
    clockout_time_full = datetime.strptime(clockout_time, "%H:%M")
    clockout_time = datetime.strptime(clockout_time, "%H:%M").time()
    
    current_time_full = datetime.now()
    current_time_only = datetime.strptime(current_time_full.strftime("%H:%M"), "%H:%M").time()
    current_time = datetime.now().time()

    allowed_time_before = (clockout_time_full - timedelta(hours=allowed_time_before_amount)).time()
    allowed_time_before = datetime.strptime(allowed_time_before.strftime("%H:%M"), "%H:%M").time()

    clockout_completed = is_clockout_in_range(allowed_time_before, clockout_time, current_time_only) 

    if clockout_completed:

        # Determine the date for the alarm entry
        if current_time < alarm_time:
            date_of_alarm = date.today()
        else:
            date_of_alarm = date.today() + timedelta(days=1)

        conn = sqlite3.connect(db_file)
        cur = conn.cursor()

        cur.execute("SELECT streak, date FROM history ORDER BY id DESC LIMIT 1")
        row = cur.fetchone() # get previous streak

        if row is None or row[1] != str(date_of_alarm - timedelta(days=1)):
            previous_streak = 0  # no previous entries or not consecutive day
        else:    
            previous_streak = row[0]
        new_streak = previous_streak + 1 # Increment streak

        data = [date_of_alarm, clockout_completed, new_streak]

        try:
            cur.execute("""
                INSERT INTO history (date, clockout, streak)
                VALUES (?, ?, ?)
            """, data)

            conn.commit()

        except sqlite3.IntegrityError as e:
            print("Error inserting clockout data:", e)

        cur.close()
        conn.close()

    else:
        print("Clockout action not in allowed time range.")

    return

# Checks if current time is within the allowed clockout range
def is_clockout_in_range(start, end, current):
    current = str(current)
    start = str(start)
    end = str(end)

    if start <= end:
        return start <= current <= end
    else:
        return start <= current or current <= end
    
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