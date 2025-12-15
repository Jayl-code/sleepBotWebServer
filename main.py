# Imports
from flask import Flask, render_template, redirect, url_for, request, jsonify, abort
import threading

from modules.get_config import get_alarm_time, get_clockout_time, get_alarm_days
from modules.alarm_thread import watch_alarm
from modules.stopping_alarm import stop_alarm_calc
from modules.handle_clockout import clockout_action
from modules.handle_habits import habit_done
from modules.get_update import get_highscore, get_score_and_streak, get_habits
from modules.update_config import save_alarm_time, save_clockout_time, save_alarm_days
from modules.get_from_db import get_all_history
from modules.update_db import delete_row, update_today

from db_setup import setup_database
from config_setup import setup_config

thread_started = False

def start_background_thread():
    global thread_started
    if not thread_started:
        thread = threading.Thread(target=watch_alarm, daemon=True)
        thread.start()
        thread_started = True

# Create config, DB and table if they don't exist
setup_database()
setup_config()

app = Flask(__name__)
start_background_thread()


# -------------------------
#         HOME
# -------------------------
@app.route('/')
def home():
    return render_template(
        'index.html',
        alarm_time=get_alarm_time(),
        clockout_time=get_clockout_time(),
        days=get_alarm_days()
    )


# -------------------------
#     AJAX UPDATE ROUTES
# -------------------------
@app.route('/update_highscore')
def update_highscore():
    return jsonify({"highscore": get_highscore()})

@app.route('/update_score_and_streak')
def update_score_and_streak():
    score, streak = get_score_and_streak()
    return jsonify({"score": score, "streak": streak})

@app.route('/update_habits')
def update_habits():
    values, is_today = get_habits()
    return jsonify({"values": values, "is_today": is_today})


# -------------------------
#      CONFIG ROUTES
# -------------------------
@app.route('/set_alarm', methods=['POST'])
def set_alarm():
    save_alarm_time(request.form['alarm_time'])
    return redirect(url_for('home'))

@app.route('/set_clockout', methods=['POST'])
def set_clockout():
    save_clockout_time(request.form['clockout_time'])
    return redirect(url_for('home'))


# -------------------------
#     CLOCKOUT + ALARM
# -------------------------
@app.route('/clockout')
def clockout():
    clockout_action()
    return redirect(url_for('home'))

@app.route('/stop_alarm', methods=['POST'])
def stop_alarm():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON received"}), 400

    stop_alarm_calc(data.get("time"), data.get("seconds"))
    return "", 202  # Accepted


# -------------------------
#      HABITS
# -------------------------
@app.route('/habit/<int:habit_id>')
def habit(habit_id):
    if habit_id not in (1, 2, 3, 4):
        abort(404)

    habit_done(habit_id)
    return "", 202


# -------------------------
#      HISTORY PAGE
# -------------------------
@app.route('/history')
def history():
    return render_template('history.html', rows=get_all_history())

@app.route('/delete_id', methods=['POST'])
def delete_id():
    delete_row(request.form['id'])
    return redirect(url_for('history'))

@app.route('/update_day', methods=['POST'])
def update_day():
    update_today(
        date=request.form['date'],
        **{request.form['column']: request.form['updated']}
    )
    return redirect(url_for('history'))


# -------------------------
#      TOGGLE DAY
# -------------------------
@app.route('/toggle_day', methods=['POST'])
def toggle_day():
    day = request.json.get("day")
    days = get_alarm_days()

    if day not in days:
        return jsonify({"error": "Invalid day"}), 400

    days[day] = not days[day]
    save_alarm_days(days)

    return jsonify({"success": True, "new_value": days[day]})


# -------------------------
#     START APP WHEN TESTING 
# -------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)
