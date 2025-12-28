# Imports
from datetime import datetime, date, timedelta

from modules.get_config import get_alarm_time, get_clockout_time, get_last_required_day
from modules.get_from_db import get_dates_history
from modules.update_db import insert_history

# File paths
config_file = 'config.json'
db_file = 'database.db'


# Processes clockout action and updates database accordingly
def clockout_action():
    allowed_time_before_amount = 3  # Hours

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

    # Determine the date for the alarm entry
    if now_time < alarm_time:
        date_of_alarm = date.today()
    else:
        date_of_alarm = date.today() + timedelta(days=1)

    alreadyClockedOut = get_dates_history(date_of_alarm, ["id"])

    if alreadyClockedOut: 
        print("Clockout already recorded for today.")
        return "0"
    
    if not get_last_required_day():
        lastHistory = None
    else:
        lastHistory = get_dates_history(get_last_required_day(), ["streak"])

    # Allowed time window (as datetime + converted to time)
    allowed_before_time = (clockout_dt - timedelta(hours=allowed_time_before_amount)).time()

    # Check if current time is within allowed clockout range
    clockout_in_range = is_clockout_in_range(allowed_before_time, clockout_time, now_time)

    if clockout_in_range:

        if lastHistory is None:
            previous_streak = 0  # no previous entries or not consecutive day
        else:    
            previous_streak = lastHistory[0] # get previous streak
        new_streak = previous_streak + 1 # Increment streak

        insert_history(
                date=date_of_alarm,
                clockout=1,
                streak=new_streak
            )
        
        return "1"

    else:
        print("Clockout action not in allowed time range.")

        return "0"

# Checks if current time is within the allowed clockout range
def is_clockout_in_range(start, end, current):
    current = str(current)
    start = str(start)
    end = str(end)

    if start <= end:
        return start <= current <= end
    else:
        return start <= current or current <= end
    