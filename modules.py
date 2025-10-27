import json
import time
from datetime import datetime

def get_config(file_path='config.json'):
    defaults = {"alarm_time": "00:00", "clockout_time": "00:00"}
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

def get_streak(file_path='streak.txt'):
    try:
        with open(file_path, 'r') as file:
            streak = int(file.read().strip())
    except (FileNotFoundError, ValueError):
        streak = 0
    return streak

def get_highscore(file_path='highscore.txt'):
    try:
        with open(file_path, 'r') as file:
            highscore = int(file.read().strip())
    except (FileNotFoundError, ValueError):
        highscore = 0
    return highscore

def get_history(file_path='history.json'):
    try:
        with open(file_path, 'r') as file:
            content = file.read().strip()
            if not content:  # empty file
                history = []
            else:
                history = json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    return history

def save_alarm_time(new_alarm_time, file_path='config.json'):
    with open(file_path, 'r') as file:
        data = json.load(file)

    data['alarm_time'] = new_alarm_time

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return

def save_clockout_time(new_clockout_time, file_path='config.json'):
    with open(file_path, 'r') as file:
        data = json.load(file)

    data['clockout_time'] = new_clockout_time

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return

def load_alarm_time(file_path='config.json'):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data.get("alarm_time", "00:00")

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

def habit_done(habit_id, file_path='history.json'):
    # todo: implement habit tracking logic here
    print(f"Habit {habit_id} marked as done.")
    return

def stop_alarm_calc(time_str, seconds_str):
    stop_alarm_playing()
    alarm_time = load_alarm_time()
    if time_str == alarm_time:
        print(f"Alarm stopped after {seconds_str} seconds.")
    else:
        print("Other")
