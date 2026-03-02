import threading
from threading import Event
import logging

log = logging.getLogger(__name__)

try:
    from light_control.sunrise import run_sunrise
    from light_control.sunset import run_sunset
    from light_control.sunrise_control import sunrise_cancel_event
    from light_control.sunset_control import sunset_cancel_event
except ImportError:
    run_sunrise = None
    run_sunset = None
    sunrise_cancel_event = Event()
    sunset_cancel_event = Event()
    log.debug("Light control not installed or incorrectly set up.")


LIGHT_CONTROL_AVAILABLE = (run_sunrise is not None and run_sunset is not None)

def start_sunset_toggle():
    if not LIGHT_CONTROL_AVAILABLE:
        log.warning("Attempted to start sunset, but light control is not available.")
        return
    
    try:
        threading.Thread(
            target=run_sunset,
            daemon=True
        ).start() 
        log.info("Sunset started successfully.")
    except Exception as e:
        log.error(f"Error starting sunset: {e}")

def start_sunrise_toggle():
    if not LIGHT_CONTROL_AVAILABLE:
        log.warning("Attempted to start sunrise, but light control is not available.")
        return
    
    try:
        threading.Thread(
            target=run_sunrise,
            daemon=True
        ).start() 
        log.info("Sunrise started successfully.")
    except Exception as e:
        log.error(f"Error starting sunrise: {e}")

def fast_finish_toggle():
    if not LIGHT_CONTROL_AVAILABLE:
        log.warning("Attempted to start fast finish, but light control is not available.")
        return
    
    try:
        sunrise_cancel_event.set()
        sunset_cancel_event.set()
        log.info("Fast finish triggered: sunrise and sunset cancelled.")
    except Exception as e:
        log.error(f"Error triggering fast finish: {e}")