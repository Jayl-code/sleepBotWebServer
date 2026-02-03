# Imports
from datetime import datetime, date, timedelta
from threading import Event
import logging

log = logging.getLogger(__name__)

from modules.get_config import get_alarm_time, get_clockout_time, get_last_required_day, get_is_light_control_enabled
from modules.get_from_db import get_dates_history
from modules.update_db import insert_history, update_today
from modules.handle_sounds import play_sound_effect

try:
    from light_control.sunset_control import sunset_cancel_event
except ImportError:
    sunset_cancel_event = Event()
    log.debug("Light control not installed or incorrectly set up.")

# File paths
config_file = 'config.json'
db_file = 'database.db'


# Processes clockout action and updates database accordingly
def clockout_action():
    if get_is_light_control_enabled():
        sunset_cancel_event.set() # Cancel any ongoing sunset

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
        log.info("Clockout already recorded for today.")
        return "0"
    
    if not get_last_required_day():
        lastHistory = None
    else:
        lastHistory = get_dates_history(get_last_required_day(), ["streak"])

    # Allowed time window (as datetime + converted to time)
    allowed_before_time = (clockout_dt - timedelta(hours=allowed_time_before_amount)).time()

    # Check if current time is within allowed clockout range
    clockout_in_range = _is_clockout_in_range(allowed_before_time, clockout_time, now_time)

    if clockout_in_range:
        log.info("Playing clockout sound effect.")
        play_sound_effect("clockout_sound")

         # Calculate new streak
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
        log.info("Clockout recorded successfully.")
        
        return "1"

    else:
        log.info("Clockout action not in allowed time range.")

        return "0"

# Checks if current time is within the allowed clockout range
def _is_clockout_in_range(start, end, current):
    current = str(current)
    start = str(start)
    end = str(end)

    if start <= end:
        return start <= current <= end
    else:
        return start <= current or current <= end
    
def clockout_failed_action():
     # Get time
    alarm_str = get_alarm_time()

    # Parse HH:MM to time and datetime
    alarm_time = datetime.strptime(alarm_str, "%H:%M").time()

    # Current time
    now = datetime.now()
    now_time = now.time()

    # Determine the date for the alarm entry
    if now_time < alarm_time:
        date_of_alarm = date.today()
    else:
        date_of_alarm = date.today() + timedelta(days=1)
    
    clockedOut = get_dates_history(date_of_alarm, ["clockout"])

    if not clockedOut or clockedOut[0] == 0:
        log.error("Not yet clocked out or already marked as failed.")
        return "0"
    
    else:
        log.info("Marking clockout as failed.")
        update_today(date=date_of_alarm,
                     clockout=0,
                     streak=0
                     )
        return "1"
