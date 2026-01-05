# Imports
import time
from datetime import datetime, timedelta
import threading

from modules.get_config import get_alarm_time, alarm_today, get_is_light_control_enabled
from modules.handle_sounds import loop_sound_toggle
from modules.get_from_db import get_dates_history

from light_control.sunrise import run_sunrise



# Watches for alarm time and triggers alarm sound when time matches 
def watch_alarm():
    last_alarm_time = None
    already_triggered_today = False
    wakeup_triggered = False
    last_day = datetime.now().day

    while True:
        now = datetime.now()

        # Reset at midnight
        if now.day != last_day:
            already_triggered_today = False
            wakeup_triggered = False
            last_day = now.day

        alarm_str = get_alarm_time()
        if alarm_str != last_alarm_time:
            # Alarm time changed
            already_triggered_today = False
            wakeup_triggered = False
            last_alarm_time = alarm_str

        alarm_hour, alarm_minute = map(int, alarm_str.split(":"))

        # Build alarm datetime
        alarm_dt = now.replace(
            hour=alarm_hour,
            minute=alarm_minute,
            second=0,
            microsecond=0
        )

        # If alarm already passed today, it must be tomorrow
        if alarm_dt <= now:
            alarm_dt += timedelta(days=1)

        # 10 minutes before alarm
        wakeup_dt = alarm_dt - timedelta(minutes=10)

        if not already_triggered_today:
            todays_history = get_dates_history(str(alarm_dt.date()), ["alarmAttempted"])
            if todays_history and todays_history[0] == 1:
                already_triggered_today = True

            else:
                # COOLDOWN LOGIC
                if get_is_light_control_enabled():
                    if now >= wakeup_dt and not wakeup_triggered:
                        threading.Thread(
                            target=run_sunrise,
                            daemon=True
                        ).start()
                        wakeup_triggered = True

                # ALARM LOGIC
                if alarm_today():
                    if (
                        now.hour == alarm_hour
                        and now.minute == alarm_minute
                        and not already_triggered_today
                    ):
                        loop_sound_toggle(True)
                        already_triggered_today = True

        time.sleep(1)