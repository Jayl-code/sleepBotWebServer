# Imports
import json
import time
from datetime import datetime, date, timedelta
import sqlite3

from modules.get_config import get_alarm_time

# File paths
config_file = 'config.json'
db_file = 'database.db'

def stop_alarm_calc(time_str, seconds_str):
    stop_alarm_playing()
    alarm_time = get_alarm_time()
    if time_str == alarm_time:
        print(f"Alarm stopped after {seconds_str} seconds.")
        points_deducted = int(seconds_str) * 16  # Example: 16 points deducted per second
        points_pre_multiplier = 1000 - points_deducted
        multiplier = get_multiplier()
        final_points = int(points_pre_multiplier * multiplier)
        
        todays_date = date.today()

        conn = sqlite3.connect(db_file)
        cur = conn.cursor()

        cur.execute("SELECT date FROM history ORDER BY id DESC LIMIT 1")
        row = cur.fetchone() # get previous date

        cur.close()
        conn.close()

        if row is None or row[0] != str(todays_date): # No entry for today yet
            date_today = str(todays_date)
            clockout_completed = 0
            alarm_stopped = 1
            stop_time = int(seconds_str)
            streak = 1
            score = final_points

            data = [date_today, clockout_completed, alarm_stopped, stop_time, streak, score]

            conn = sqlite3.connect(db_file)
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO history (date, clockout, alarmStopped, stopTime, streak, score)
                VALUES (?, ?, ?, ?, ?, ?)
            """, data)
            conn.commit()

            cur.close()
            conn.close()

        else:
            # Update existing entry for today
            alarm_stopped = 1
            stop_time = int(seconds_str)
            score = final_points
            date_today = str(todays_date)

            data = [alarm_stopped, stop_time, score, date_today]

            conn = sqlite3.connect(db_file)
            cur = conn.cursor()

            cur.execute("""
                UPDATE history
                SET alarmStopped = ?, stopTime = ?, score = ?
                WHERE date = ?
            """, data)
            conn.commit()

            cur.close()
            conn.close()


    else:
        print("Other")
        # todo: set streak of day to 0 in database
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()

        cur.execute("SELECT date, id FROM history ORDER BY id DESC LIMIT 1")
        row = cur.fetchone() # get previous date

        cur.close()
        conn.close()

        if row[0] == str(date.today()):
            alarm_stopped = 0
            data = [alarm_stopped, row[0]]
            conn = sqlite3.connect(db_file)
            cur = conn.cursor()

            cur.execute("""
                UPDATE history
                SET alarmStopped = ?
                WHERE date = ?
            """, data)
            conn.commit()

            cur.close()
            conn.close()

        else:
            pass

    return

# Stops alarm sound (placeholder function)
def stop_alarm_playing():
    print("Stopping alarm sound...")
    # todo: implement actual sound stopping logic here
    return

def get_current_streak():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.execute("SELECT streak, date FROM history ORDER BY id DESC LIMIT 1")
    row = cur.fetchone() # get previous streak

    cur.close()
    conn.close()

    if row is None or row[1] != str(date.today() - timedelta(days=1)):
        return 0  # no previous entries or not consecutive day
    else:
        return row[0]

def get_multiplier():
    previous_streak = get_current_streak()

    date_today = date.today()

    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.execute("SELECT clockout, date FROM history ORDER BY id DESC LIMIT 1")
    row = cur.fetchone() # get previous streak

    cur.close()
    conn.close()

    if row is None or row[1] != str(date_today) or row[0] == 0:
        previous_streak = 0  # no previous entries or clockout not completed today

    if previous_streak > 0:
        multiplier_amount = int(previous_streak) / 10
        multiplier = 1 + multiplier_amount
    else:
        multiplier = 1

    return multiplier