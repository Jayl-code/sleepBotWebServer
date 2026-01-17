# time_thread.py

# Imports
import time
from datetime import datetime, timedelta
import threading
import logging

from modules.get_config import get_alarm_time, alarm_today, get_is_light_control_enabled, get_clockout_time
from modules.handle_sounds import loop_sound_toggle
from modules.get_from_db import get_dates_history
from modules.notifications import send_notification, keys_file_there

from light_control.sunrise import run_sunrise
from light_control.sunset import run_sunset

log = logging.getLogger(__name__)

# Watches for set times and triggers alarm sound when time matches 
def watch_times():
    log.info("Starting watch_times thread")

    last_alarm_time = None
    last_clockout_time = None

    alarm_triggered_today = False
    clockout_triggered_today = False

    wakeup_triggered = False
    cooldown_triggered = False

    last_day = datetime.now().day

    while True:
        try:
            now = datetime.now()

            # Reset at midnight
            if now.day != last_day:
                alarm_triggered_today = False
                clockout_triggered_today = False
                wakeup_triggered = False
                cooldown_triggered = False
                last_day = now.day

            # Get current alarm and clockout times from config file
            alarm_str = get_alarm_time()
            clockout_str = get_clockout_time()

            if alarm_str != last_alarm_time:
                # Alarm time changed so reset triggers
                alarm_triggered_today = False
                wakeup_triggered = False
                last_alarm_time = alarm_str

            if clockout_str != last_clockout_time:
                # Clockout time changed so reset triggers
                clockout_triggered_today = False
                cooldown_triggered = False
                last_clockout_time = clockout_str

            try:
                alarm_hour, alarm_minute = map(int, alarm_str.split(":"))
                clockout_hour, clockout_minute = map(int, clockout_str.split(":"))
            except ValueError:
                # Config file has invalid time format
                log.error("Invalid time format: alarm=%s clockout=%s", alarm_str, clockout_str)
                time.sleep(5)
                continue

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
                # Check DB if alarm already triggered today
                todays_alarm_history = get_dates_history(str(alarm_dt.date()), ["alarmAttempted"])
                if todays_alarm_history and todays_alarm_history[0] == 1:
                    alarm_triggered_today = True

                else:
                    # WAKEUP LOGIC
                    if get_is_light_control_enabled():
                        if now >= wakeup_dt and not wakeup_triggered:
                            log.info("Starting sunrise from watch_times thread")
                            wakeup_triggered = True
                            threading.Thread(
                                target=run_sunrise,
                                daemon=True
                            ).start()         

                    # ALARM LOGIC
                    if alarm_today():
                        if now >= alarm_dt and not alarm_triggered_today:
                            log.info("Triggering alarm from watch_times thread")
                            alarm_triggered_today = True
                            loop_sound_toggle(True)
                            
            if not clockout_triggered_today:
                # Check DB if clockout already triggered today
                todays_clockout_history = get_dates_history(str(clockout_dt.date()), ["clockout"])
                if todays_clockout_history and todays_clockout_history[0] == 1:
                    clockout_triggered_today = True

                else:
                    # COOLDOWN LOGIC
                    if now >= cooldown_dt and not cooldown_triggered:
                        # Check for keys file before sending notification
                        if keys_file_there():
                            log.info("Sending clockout notification from watch_times thread")
                            send_notification() # Send notification to users phone to start cooldown
                        if get_is_light_control_enabled():
                            log.info("Starting sunset from watch_times thread")
                            threading.Thread(
                                target=run_sunset,
                                daemon=True
                            ).start()
                        cooldown_triggered = True

            time.sleep(1)
        
        except Exception:
            log.exception("Error in watch_times thread")
            time.sleep(5)