# Imports
from datetime import datetime, date, timedelta
import sqlite3

from modules.get_config import *

# File paths
config_file = 'config.json'
db_file = 'database.db'


# Processes clockout action and updates database accordingly
def clockout_action():
    date_of_alarm = None
    clockout_completed = None

    allowed_time_before_amount = 4  # Hours

    # Get times
    alarm_str = get_alarm_time()
    clockout_str = get_clockout_time()

    # Parse HH:MM to time and datetime
    alarm_time = datetime.strptime(alarm_str, "%H:%M").time()
    clockout_dt = datetime.strptime(clockout_str, "%H:%M")   # full datetime
    clockout_time = clockout_dt.time()

    # Current time
    now = datetime.now()
    now_time = now.time()

    # Allowed time window (as datetime + converted to time)
    allowed_before_time = (clockout_dt - timedelta(hours=allowed_time_before_amount)).time()

    # Check if current time is within allowed clockout range
    clockout_in_range = is_clockout_in_range(allowed_before_time, clockout_time, now_time)

    if clockout_in_range:

        # Determine the date for the alarm entry
        if now_time < alarm_time:
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
    