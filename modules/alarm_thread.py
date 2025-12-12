# Imports
import time
from datetime import datetime

from modules.get_config import get_alarm_time, alarm_today
from modules.handle_sounds import loop_sound_toggle


# Watches for alarm time and triggers alarm sound when time matches 
def watch_alarm():
    last_alarm_time = None
    already_triggered_today = False
    last_day = datetime.now().day

    while True:
        now = datetime.now()

        # Reset at midnight
        if now.day != last_day:
            already_triggered_today = False
            last_day = now.day

        alarm_str = get_alarm_time()
        if alarm_str != last_alarm_time:
            # Alarm time changed!
            already_triggered_today = False
            last_alarm_time = alarm_str

        if alarm_today():
            alarm_hour, alarm_minute = map(int, alarm_str.split(":"))
            if (now.hour == alarm_hour and now.minute == alarm_minute and not already_triggered_today):
                loop_sound_toggle(True)
                already_triggered_today = True

        time.sleep(1)