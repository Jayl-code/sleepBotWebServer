# Imports
import time
from datetime import datetime, timedelta
import threading

from modules.get_config import get_alarm_time, alarm_today, get_is_light_control_enabled, get_clockout_time
from modules.handle_sounds import loop_sound_toggle
from modules.get_from_db import get_dates_history
from modules.notifications import send_notification, keys_file_there

from light_control.sunrise import run_sunrise
from light_control.sunset import run_sunset



# Watches for alarm time and triggers alarm sound when time matches 
def watch_alarm():
    last_alarm_time = None
    last_clockout_time = None

    alarm_triggered_today = False
    clockout_triggered_today = False

    wakeup_triggered = False
    cooldown_triggered = False

    last_day = datetime.now().day

    while True:
        now = datetime.now()

        # Reset at midnight
        if now.day != last_day:
            alarm_triggered_today = False
            clockout_triggered_today = False
            wakeup_triggered = False
            cooldown_triggered = False
            last_day = now.day

        alarm_str = get_alarm_time()
        clockout_str = get_clockout_time()

        if alarm_str != last_alarm_time:
            # Alarm time changed
            alarm_triggered_today = False
            wakeup_triggered = False
            last_alarm_time = alarm_str

        if clockout_str != last_clockout_time:
            # Clockout time changed
            clockout_triggered_today = False
            cooldown_triggered = False
            last_clockout_time = clockout_str

        alarm_hour, alarm_minute = map(int, alarm_str.split(":"))
        clockout_hour, clockout_minute = map(int, clockout_str.split(":"))

        # Build alarm datetime
        alarm_dt = now.replace(
            hour=alarm_hour,
            minute=alarm_minute,
            second=0,
            microsecond=0
        )

        # Build clockout datetime
        clockout_dt = now.replace(
            hour=clockout_hour,
            minute=clockout_minute,
            second=0,
            microsecond=0
        )

        # If alarm already passed today, it must be tomorrow
        if alarm_dt <= now:
            alarm_dt += timedelta(days=1)

        # If clockout already passed today, it must be tomorrow
        if clockout_dt <= now:
            clockout_dt += timedelta(days=1)

        # 10 minutes before alarm
        wakeup_dt = alarm_dt - timedelta(minutes=10)

        # 1 hour before clockout
        cooldown_dt = clockout_dt - timedelta(minutes=60)

        if not alarm_triggered_today:
            todays_alarm_history = get_dates_history(str(alarm_dt.date()), ["alarmAttempted"])
            if todays_alarm_history and todays_alarm_history[0] == 1:
                alarm_triggered_today = True

            else:
                # WAKEUP LOGIC
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
                        and not alarm_triggered_today
                    ):
                        loop_sound_toggle(True)
                        alarm_triggered_today = True

        if not clockout_triggered_today:
            todays_clockout_history = get_dates_history(str(clockout_dt.date()), ["clockout"])
            if todays_clockout_history and todays_clockout_history[0] == 1:
                clockout_triggered_today = True

            else:
                # COOLDOWN LOGIC
                if now >= cooldown_dt and not cooldown_triggered:
                    if keys_file_there():
                        send_notification()
                    if get_is_light_control_enabled():
                        threading.Thread(
                            target=run_sunset,
                            daemon=True
                        ).start()
                    cooldown_triggered = True

        time.sleep(1)