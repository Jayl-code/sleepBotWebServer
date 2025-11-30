# Imports
from datetime import date, timedelta

from modules.get_config import get_alarm_time
from modules.get_from_db import *
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

    lastHistory = get_last_history()

    if lastHistory and lastHistory[0] == str(date.today() + timedelta(days=1)):
        print("Future clockout entry exists, cannot stop alarm for today.")
        return
    
    lastHistoryToday = True if lastHistory and lastHistory[0] == dateToday else False

    if lastHistoryToday and lastHistory[4] == 1:
        print("Alarm already stopped for today.")
        return

    if time_str == alarm_time:
        print(f"Alarm stopped after {seconds} seconds.")

        multiplier, currentStreak = get_multiplier(lastHistory) if lastHistoryToday else (1, 1)

        # Score calculation
        points_deducted = seconds * 16 # 16 points deducted per second
        base_points = 1000 - points_deducted
        final_score = int(base_points * multiplier)

        # If no entry today then create new
        if not lastHistoryToday:
            insert_history(
                date=dateToday,
                clockout=0,
                alarmStopped=1,
                stopTime=seconds,
                streak=1,
                score=final_score,
                alarmAttempted=1
            )
        else:
            # Update existing row for today
            update_today(
                alarmStopped=1,
                stopTime=seconds,
                score=final_score,
                streak=currentStreak,
                alarmAttempted=1,
                dateToday=dateToday
            )

        return
    
    if lastHistoryToday:
        # Update existing row: failed alarm
        update_today(
            alarmStopped=0,
            stopTime=0,
            score=0,
            streak=0,
            alarmAttempted=1,
            dateToday=dateToday
        )
    else:
        # No row for today yet then insert zeroed-out fail row
        insert_history(
            date=dateToday,
            clockout=0,
            alarmStopped=0,
            stopTime=0,
            streak=0,
            score=0,
            alarmAttempted=1
        )

        return

    return

def get_multiplier(last_history,):
    current_streak = last_history[2]

    if current_streak > 0:
        multiplier_amount = int(current_streak) / 10
        multiplier = 1 + multiplier_amount
    else:
        multiplier = 1
    print(multiplier)    

    return multiplier, current_streak