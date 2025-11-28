# Imports
import time
from datetime import datetime

from modules.get_config import get_alarm_time
from modules.handle_sounds import play_sound


# Watches for alarm time and triggers alarm sound when time matches 
def watch_alarm():
    last_triggered_minute = None
    while True:
        try:
            alarm_str = get_alarm_time()
            now = datetime.now()
            current_str = now.strftime("%H:%M")

            # Avoid triggering multiple times per minute
            if current_str == alarm_str and last_triggered_minute != current_str:
                play_sound()
                last_triggered_minute = current_str

        except Exception as e:
            print("Error:", e)

        time.sleep(1) #todo: variable sleep time
