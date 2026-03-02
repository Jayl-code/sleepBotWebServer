# main.py

# Imports
from flask import Flask, render_template, redirect, url_for, request, jsonify, abort
import threading
import sys
import logging

log = logging.getLogger(__name__)

from modules.get_config import get_alarm_time, get_clockout_time, get_alarm_days
from modules.time_thread import watch_times
from modules.stopping_alarm import stop_alarm_calc
from modules.handle_clockout import clockout_action, clockout_failed_action
from modules.handle_habits import habit_done
from modules.get_update import get_current_streak, get_current_habits, get_current_score
from modules.update_config import save_alarm_time, save_clockout_time, save_alarm_days
from modules.get_from_db import get_all_history, get_current_highscore
from modules.update_db import delete_row, update_today

from db_setup import setup_database
from config_setup import setup_config


# Create config, DB and DB table if they don't exist
try:
    setup_database()
except Exception:
    log.exception("Failed to set up database on startup")
    sys.exit(1)

try:
    setup_config()
except Exception:
    log.exception("Failed to set up config on startup")
    sys.exit(1)

# Initialize Flask app
app = Flask(__name__)

# Start background thread to watch times
thread_started = False

def start_background_thread():
    global thread_started
    if not thread_started:
        try:
            thread = threading.Thread(target=watch_times, daemon=True)
            thread.start()
            thread_started = True
        except Exception:
            log.exception("Failed to start background thread")
            sys.exit(1)

start_background_thread()


# -------------------------
#         HOME PAGE
# -------------------------
@app.route('/')
def home():
    log.info("Rendering home page")

    try:
        # Getting data for rendering
        alarm_time=get_alarm_time()
        clockout_time=get_clockout_time()
        alarm_days=get_alarm_days()
        highscore=get_current_highscore()
        score=get_current_score()
        streakActive, streak=get_current_streak()
        habitsActive, habits = get_current_habits()
    
    except Exception:
        log.exception("Error getting data for home page") 
        return "Error loading page", 500    
    
    return render_template(
        'index.html',
        alarm_time=alarm_time,
        clockout_time=clockout_time,
        alarm_days=alarm_days,
        highscore=highscore,
        score=score,
        streakActive=streakActive,
        streak=streak,
        habitsActive=habitsActive,
        habits=habits
    )


# -------------------------
#      CONFIG ROUTES
# -------------------------
@app.route('/set_alarm', methods=['POST'])
def set_alarm():
    # Called by form on home page to set new alarm time
    log.info("Set new alarm time route called")
    
    alarm_time = request.form.get('alarm_time')
    if not alarm_time:
        log.warning("alarm_time not provided")
        return redirect(url_for('home'))
    
    try:
        save_alarm_time(alarm_time)
    except Exception as e:
        log.error(f"Failed to save alarm time: {e}")
    
    return redirect(url_for('home'))

@app.route('/set_clockout', methods=['POST'])
def set_clockout():
    # Called by form on home page to set new clockout time
    log.info("Set new clockout time route called")
    
    clockout_time = request.form.get('clockout_time')
    if not clockout_time:
        log.warning("clockout_time not provided")
        return redirect(url_for('home'))
    
    try:
        save_clockout_time(clockout_time)
    except Exception as e:
        log.error(f"Failed to save clockout time: {e}")
    
    return redirect(url_for('home'))


# -------------------------
#     CLOCKOUT, CLOCKOUT FAILED, AND ALARM STOP
# -------------------------
@app.route('/clockout')
def clockout():
    # Called by iPhone shortcuts app to perform clockout action
    log.info("Clockout route called")
    try:
        return clockout_action()
    except Exception as e:
        log.error(f"Failed to perform clockout action: {e}")
    return "0"

@app.route('/clockout_failed')
def clockout_failed():
    # Called by iPhone shortcuts app when clockout fails
    log.info("Clockout failed route called")
    try:
        return clockout_failed_action()
    except Exception as e:
        log.error(f"Failed to perform clockout failed action: {e}")
        return "0"

@app.route('/stop_alarm', methods=['POST'])
def stop_alarm():
    # Controller sends JSON with time and seconds when stopping alarm
    data = request.get_json()
    if not data:
        log.warning("No JSON data received in stop_alarm")
        return jsonify({"error": "No JSON received"}), 400
    
    try:
        stop_alarm_calc(data.get("time"), data.get("seconds"))
        log.info(f"Stopping alarm: {data}")
    except Exception as e:
        log.error(f"Failed to stop alarm: {e}")

    return "", 202  # Accepted


# -------------------------
#      HABITS
# -------------------------
@app.route('/habit/<int:habit_id>')
def habit(habit_id):
    # Controller calls this route with habit ID to mark as done
    if habit_id not in (1, 2, 3, 4):
        log.warning(f"Invalid habit ID received: {habit_id}")
        abort(404)

    try:
        log.info(f"Habit route called for habit ID: {habit_id}")
        habit_done(habit_id)
    except Exception as e:
        log.error(f"Failed to mark habit {habit_id} as done: {e}")
    
    return "", 202 # Accepted


# -------------------------
#      TOGGLE DAY
# -------------------------
@app.route('/toggle_day', methods=['POST'])
def toggle_day():
    # Called by JS to toggle a day on/off for alarm
    data = request.get_json()

    if not data or "day" not in data:
        log.warning("No day provided in toggle_day")
        return jsonify({"error": "Missing day"}), 400

    day = data["day"]
    
    try:
        days = get_alarm_days()

        if day not in days:
            log.warning(f"Invalid day provided in toggle_day: {day}")
            return jsonify({"error": "Invalid day"}), 400

        days[day] = not days[day]
        save_alarm_days(days)
        log.info(f"Toggled day {day} to {days[day]}")
        return jsonify({"success": True, "new_value": days[day]})
    except Exception as e:
        log.error(f"Failed to toggle day {day}: {e}")
        return jsonify({"error": "Failed to toggle day"}), 500


# -------------------------
#      HISTORY PAGE
# -------------------------
@app.route('/history')
def history():
    try:
        rows = get_all_history()
    except Exception as e:
        log.error(f"Failed to get history: {e}")
        rows = []
    
    return render_template('history.html', rows=rows)

@app.route('/delete_id', methods=['POST'])
def delete_id():
    row_id = request.form.get('id')
    if not row_id:
        log.warning("id not provided")
        return redirect(url_for('history'))
    
    try:
        delete_row(int(row_id))
        log.info(f"Deleted row with ID: {row_id}")
    except (ValueError, Exception) as e:
        log.error(f"Failed to delete row: {e}")
    
    return redirect(url_for('history'))

@app.route('/update_day', methods=['POST'])
def update_day():
    date = request.form.get('date')
    column = request.form.get('column')
    updated = request.form.get('updated')
    
    if not date or not column or updated is None:
        log.warning("Missing required fields")
        return redirect(url_for('history'))
    
    try:
        update_today(date=date, **{column: updated})
        log.info(f"Updated {column} for date {date}")
    except Exception as e:
        log.error(f"Failed to update: {e}")
    
    return redirect(url_for('history'))


# -------------------------
#     START APP WHEN TESTING 
# -------------------------
# if __name__ == '__main__':
#     from logging_config import setup_logging
#     setup_logging()
#     log.debug("Starting app in debug mode")
#     app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)
