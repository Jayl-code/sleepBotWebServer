# Imports
import time
from datetime import datetime
import json

config_file = 'config.json'

# Watches for alarm time and triggers alarm sound when time matches 
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

# Plays alarm sound (placeholder function)
def play_sound():
    print("Playing sound...")
    # todo: implement actual sound playing logic here
    return

# Loads alarm time from config file
def load_alarm_time(file_path=config_file):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data.get("alarm_time", "00:00")