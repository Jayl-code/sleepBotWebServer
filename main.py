# main.py

# Imports
from flask import Flask, render_template, redirect, url_for, request, jsonify, abort
import threading
import logging

from modules.get_config import get_alarm_time, get_clockout_time, get_alarm_days, get_is_light_control_enabled
from modules.time_thread import watch_times
from modules.stopping_alarm import stop_alarm_calc
from modules.handle_clockout import clockout_action
from modules.handle_habits import habit_done
from modules.get_update import get_current_streak, get_current_habits, get_current_score
from modules.update_config import save_alarm_time, save_clockout_time, save_alarm_days, toggle_light_control
from modules.get_from_db import get_all_history, get_current_highscore
from modules.update_db import delete_row, update_today

from db_setup import setup_database
from config_setup import setup_config

log = logging.getLogger(__name__)

# Create config, DB and DB table if they don't exist
setup_database()
setup_config()

# Initialize Flask app
app = Flask(__name__)

# Start background thread to watch times
thread_started = False

def start_background_thread():
    global thread_started
    if not thread_started:
        thread = threading.Thread(target=watch_times, daemon=True)
        thread.start()
        thread_started = True

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
        light_mode=get_is_light_control_enabled()
        highscore=get_current_highscore()
        score=get_current_score()
        streakActive, streak=get_current_streak()
        habitsActive, habits = get_current_habits()
    
    except Exception:
        log.exception("Error getting data for home page")     
    
    return render_template(
        'index.html',
        alarm_time=alarm_time,
        clockout_time=clockout_time,
        alarm_days=alarm_days,
        light_mode=light_mode,
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
    log.info("Set new alarm time route called")
    save_alarm_time(request.form['alarm_time'])
    return redirect(url_for('home'))

@app.route('/set_clockout', methods=['POST'])
def set_clockout():
    log.info("Set new clockout time route called")
    save_clockout_time(request.form['clockout_time'])
    return redirect(url_for('home'))


# -------------------------
#       TOGGLE LIGHT CONTROL
# -------------------------
@app.route('/toggle_light_mode', methods=['GET'])
def toggle_light_mode():
    toggle_light_control()
    log.info("Toggled light control mode")
    return redirect(url_for('home'))


# -------------------------
#     CLOCKOUT + ALARM STOP
# -------------------------
@app.route('/clockout')
def clockout():
    log.info("Clockout route called")
    return clockout_action()

@app.route('/stop_alarm', methods=['POST'])
def stop_alarm():
    # Controller sends JSON with time and seconds when stopping alarm
    data = request.get_json()
    if not data:
        log.warning("No JSON data received in stop_alarm")
        return jsonify({"error": "No JSON received"}), 400
    
    log.info(f"Stopping alarm route reached with: {data}")

    stop_alarm_calc(data.get("time"), data.get("seconds"))
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

    log.info(f"Habit route called for habit ID: {habit_id}")
    habit_done(habit_id)
    return "", 202


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
    days = get_alarm_days()

    if day not in days:
        log.warning(f"Invalid day provided in toggle_day: {day}")
        return jsonify({"error": "Invalid day"}), 400

    # Toggle the day (True/False)
    days[day] = not days[day]
    save_alarm_days(days)

    log.info(f"Toggled day {day} to {days[day]}")
    return jsonify({"success": True, "new_value": days[day]})


# -------------------------
#      HISTORY PAGE
# -------------------------
@app.route('/history')
def history():
    return render_template('history.html', rows=get_all_history())

@app.route('/delete_id', methods=['POST'])
def delete_id():
    delete_row(request.form['id'])
    log.info(f"Deleted row with ID: {request.form['id']}")
    return redirect(url_for('history'))

@app.route('/update_day', methods=['POST'])
def update_day():
    update_today(
        date=request.form['date'],
        **{request.form['column']: request.form['updated']}
    )
    log.info(f"Updated {request.form['column']} for date {request.form['date']} to {request.form['updated']}")
    return redirect(url_for('history'))


# -------------------------
#     START APP WHEN TESTING 
# -------------------------
#if __name__ == '__main__':
#    log.debug("Starting app in debug mode")
#    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)
