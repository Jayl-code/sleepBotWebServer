

# Imports
import subprocess
import threading
import time
import os
import logging

log = logging.getLogger(__name__)

# Create a lock to protect access to shared variables
_lock = threading.Lock()

_looping = False
_loop_thread = None
_current_process = None

def loop_sound_toggle(run: bool, filename="static/sounds/alarm_sound.wav", max_time=300):
    log.info("loop_sound_toggle called with run=%s", run)
    global _looping, _loop_thread, _current_process

    # STOP
    if not run:
        with _lock:  # Acquire lock before accessing shared variables
            _looping = False
            proc = _current_process  # Get reference while locked
        
        if proc:
            try:
                if proc.poll() is None:
                    proc.terminate()
                    log.info("Terminated sound process.")
            except Exception:
                log.exception("Error terminating sound process.")
        return

    # Already running
    with _lock:
        if _looping:
            log.debug("Sound already looping, ignoring start request")
            return
        # Start looping
        _looping = True

    # Validate file exists before starting thread
    if not os.path.exists(filename):
        log.error(f"Sound file not found: {filename}")
        with _lock:
            _looping = False
        return

    def loop_thread_func():
        global _looping, _current_process
        start_time = time.time()

        try:
            while True:
                # Check looping status safely
                with _lock:
                    elapsed = time.time() - start_time
                    if not _looping or elapsed >= max_time:
                        if elapsed >= max_time:
                            log.info(f"Sound loop reached max time ({max_time}s)")
                        break
                
                # Start subprocess with error handling
                try:
                    _current_process = subprocess.Popen(["/usr/bin/aplay", filename]) # aplay for use on Pi, afplay when testing on mac
                    log.debug(f"Started aplay process (PID: {_current_process.pid})")
                except FileNotFoundError:
                    log.error("aplay not found at /usr/bin/aplay. Install it or check the path.")
                    with _lock:
                        _looping = False
                    break
                except Exception as e:
                    log.error(f"Failed to start aplay: {e}")
                    with _lock:
                        _looping = False
                    break
                
                # Wait for process to complete or be terminated
                while True:
                    try:
                        with _lock:
                            should_stop = not _looping
                        
                        if should_stop:
                            break
                        
                        if _current_process.poll() is not None:
                            log.debug("Sound finished playing (cycle complete)")
                            break
                    except Exception as e:
                        log.error(f"Error checking process status: {e}")
                        break
                    
                    time.sleep(0.05)

                # Terminate if still running and looping was stopped
                try:
                    if _current_process and _current_process.poll() is None:
                        _current_process.terminate()
                except Exception as e:
                    log.error(f"Error terminating process: {e}")

        except Exception as e:
            log.exception(f"Unexpected error in sound loop: {e}")
        
        finally:
            # Ensure cleanup happens no matter what
            try:
                with _lock:
                    if _current_process and _current_process.poll() is None:
                        _current_process.terminate()
                    _looping = False
                    _current_process = None
                elapsed = time.time() - start_time
                log.info(f"Sound loop stopped after {elapsed:.1f}s")
            except Exception as e:
                log.error(f"Error in cleanup: {e}")

    _loop_thread = threading.Thread(target=loop_thread_func, daemon=True)
    _loop_thread.start()
