# Imports
from datetime import date

from modules.get_config import get_alarm_time
from modules.get_from_db import get_dates_history
from modules.handle_sounds import stop_alarm_playing
from modules.update_db import *

# File paths
config_file = 'config.json'
db_file = 'database.db'

def stop_alarm_calc(time_str, seconds_str):
    stop_alarm_playing()

    alarm_time = get_alarm_time()
    dateToday = str(date.today())
    seconds = int(seconds_str)

    todays_history = get_dates_history(dateToday, ["alarmAttempted", "streak"])
    
    historyToday = True if todays_history else False

    if historyToday and todays_history[0] == 1:
        print("Alarm already stopped for today.")
        return

    if time_str == alarm_time:
        print(f"Alarm stopped after {seconds} seconds.")

        multiplier = get_multiplier(todays_history) if historyToday else 1

        # Score calculation
        points_deducted = seconds * 16 # 16 points deducted per second
        base_points = 1000 - points_deducted
        final_score = int(base_points * multiplier)

        # If no entry today then create new
        if not historyToday:
            insert_history(
                date=dateToday,
                alarmStopped=1,
                stopTime=seconds,
                streak=1,
                score=final_score,
                alarmAttempted=1
            )
        else:
            # Update existing row for today
            update_today(
                date=dateToday,
                alarmStopped=1,
                stopTime=seconds,
                score=final_score,
                alarmAttempted=1
            )

        return
    
    if historyToday:
        # Update existing row: failed alarm
        update_today(
            date=dateToday,
            alarmStopped=0,
            stopTime=0,
            score=0,
            streak=0,
            alarmAttempted=1
        )
    else:
        # No row for today yet then insert zeroed-out fail row
        insert_history(
            date=dateToday,
            alarmStopped=0,
            stopTime=0,
            streak=0,
            score=0,
            alarmAttempted=1
        )

        return

    return

def get_multiplier(last_history,):
    current_streak = last_history[1]

    if current_streak > 0:
        multiplier_amount = int(current_streak) / 10
        multiplier = 1 + multiplier_amount
    else:
        multiplier = 1
    print(multiplier)    

    return multiplier