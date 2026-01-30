# Imports
from datetime import datetime, date, timedelta
from threading import Event
import logging

log = logging.getLogger(__name__)

from modules.get_config import get_alarm_time, get_is_light_control_enabled
from modules.get_from_db import get_dates_history
from modules.handle_sounds import loop_sound_toggle
from modules.update_db import insert_history, update_today

try:
    from light_control.sunrise_control import sunrise_cancel_event
except ImportError:
    sunrise_cancel_event = Event()
    log.debug("Light control not installed or incorrectly set up.")


# File paths
config_file = 'config.json'
db_file = 'database.db'

def build_time_datetime(time_str, alarm_time):
    #Returns a datetime for time_str that correctly aligns
    #with the alarm datetime, even across midnight.
    today = date.today()

    alarm_dt = datetime.strptime(
        f"{today} {alarm_time}",
        "%Y-%m-%d %H:%M"
    )

    time_dt = datetime.strptime(
        f"{today} {time_str}",
        "%Y-%m-%d %H:%M"
    )

    # If time is later than alarm, it must be from the previous day
    if time_dt > alarm_dt:
        time_dt -= timedelta(days=1)

    return time_dt, alarm_dt

def stop_alarm_calc(time_str, seconds_str):
    loop_sound_toggle(False)

    if get_is_light_control_enabled():
        sunrise_cancel_event.set()

    alarm_time = get_alarm_time()
    dateToday = str(date.today())
    seconds = int(seconds_str)

    # To see of clockout was compleated today and then if alarm has already been attempted
    todays_history = get_dates_history(dateToday, ["alarmAttempted", "streak"])
    historyToday = True if todays_history else False

    if historyToday and todays_history is not None and todays_history[0] == 1:
        log.info("Alarm already stopped for today.")
        return
    
    time_dt, alarm_dt = build_time_datetime(time_str, alarm_time)
    window_start = alarm_dt - timedelta(hours=4)

    if window_start <= time_dt <= alarm_dt:
        # If early, zero seconds
        effective_seconds = 0 if time_dt < alarm_dt else seconds

        log.info(f"Alarm stopped after {effective_seconds} seconds.")

        multiplier = _get_multiplier(todays_history) if historyToday else 1

        # Score calculation
        points_deducted = effective_seconds * 16 # 16 points deducted per second
        base_points = 1000 - points_deducted
        final_score = int(base_points * multiplier)

        # If no entry today then create new
        if not historyToday:
            insert_history(
                date=dateToday,
                alarmStopped=1,
                stopTime=effective_seconds,
                streak=1,
                score=final_score,
                alarmAttempted=1
            )
        else:
            # Update existing row for today
            update_today(
                date=dateToday,
                alarmStopped=1,
                stopTime=effective_seconds,
                score=final_score,
                alarmAttempted=1
            )

        return
    
    if historyToday:
        # Update existing row: failed alarm
        update_today(
            date=dateToday,
            alarmStopped=0,
            score=0,
            streak=0,
            alarmAttempted=1
        )
    else:
        # No row for today yet then insert zeroed-out fail row
        insert_history(
            date=dateToday,
            alarmStopped=0,
            streak=0,
            score=0,
            alarmAttempted=1
        )

        return

    return

def _get_multiplier(history):
    current_streak = history[1]

    if current_streak > 0:
        multiplier_amount = int(current_streak) / 10
        multiplier = 1 + multiplier_amount
    else:
        multiplier = 1  

    return multiplier