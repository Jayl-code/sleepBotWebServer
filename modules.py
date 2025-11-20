import json
import time
from datetime import datetime, date, timedelta
import sqlite3


config_file = 'config.json'
db_file = 'database.db'


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


def save_alarm_time(new_alarm_time, file_path=config_file):
    with open(file_path, 'r') as file:
        data = json.load(file)

    data['alarm_time'] = new_alarm_time

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return

def save_clockout_time(new_clockout_time, file_path=config_file):
    with open(file_path, 'r') as file:
        data = json.load(file)

    data['clockout_time'] = new_clockout_time

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return

def load_alarm_time(file_path=config_file):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data.get("alarm_time", "00:00")

def clockout_action():
    date_of_alarm = None
    clockout_completed = 1

    alarm_time = load_alarm_time()
    alarm_time = datetime.strptime(alarm_time, "%H:%M").time()
    current_time = datetime.now().time()

    if current_time < alarm_time:
        date_of_alarm = date.today()
    else:
        date_of_alarm = date.today() + timedelta(days=1)

    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.execute("SELECT streak FROM history ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()

    if row is None:
        previous_streak = 0  # no previous entries
    else:    
        previous_streak = row[0]
    new_streak = previous_streak + 1

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

    return

def play_sound():
    print("Playing sound...")
    # todo: implement actual sound playing logic here

def stop_alarm_playing():
    print("Stopping alarm sound...")
    # todo: implement actual sound stopping logic here
    return

def watch_alarm():
    last_triggered_minute = None
    while True:
        try:
            alarm_str = load_alarm_time()
            now = datetime.now()
            current_str = now.strftime("%H:%M")

            # Avoid triggering multiple times per minute
            if current_str == alarm_str and last_triggered_minute != current_str:
                play_sound()
                last_triggered_minute = current_str

        except Exception as e:
            print("Error:", e)

        time.sleep(1)

def stop_alarm_calc(time_str, seconds_str):
    stop_alarm_playing()
    alarm_time = load_alarm_time()
    if time_str == alarm_time:
        print(f"Alarm stopped after {seconds_str} seconds.")
        # todo: implement logic to update history, streak, highscore here
    else:
        print("Other")
    return

def habit_done(habit_id):
    # todo: implement habit tracking logic here
    print(f"Habit {habit_id} marked as done.")
    return
