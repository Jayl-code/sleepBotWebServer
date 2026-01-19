import subprocess
import threading
import time
import logging

log = logging.getLogger(__name__)

_looping = False
_loop_thread = None
_current_process = None

def loop_sound_toggle(run: bool, filename="static/sounds/alarm_sound.wav", max_time=300):
    log.info("loop_sound_toggle called with run=%s", run)
    global _looping, _loop_thread, _current_process

    # STOP
    if not run:
        _looping = False
        if _current_process and _current_process.poll() is None:
            _current_process.terminate()
        return

    # Already running
    if _looping:
        return

    # START
    _looping = True

    def loop_thread_func():
        global _looping, _current_process
        start_time = time.time()

        while _looping and (time.time() - start_time < max_time):
            _current_process = subprocess.Popen(["/usr/bin/aplay", filename]) # aplay for use on Pi, afplay when testing on mac
            while _looping and _current_process.poll() is None:
                time.sleep(0.05)

            if not _looping and _current_process.poll() is None:
                _current_process.terminate()

        _looping = False
        _current_process = None

    _loop_thread = threading.Thread(target=loop_thread_func, daemon=True)
    _loop_thread.start()
