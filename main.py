# Imports
from flask import Flask, render_template, redirect, url_for, request, jsonify, abort 
import threading

from modules.get_config import get_alarm_time, get_clockout_time
from modules.alarm_thread import watch_alarm
from modules.stopping_alarm import stop_alarm_calc
from modules.handle_clockout import clockout_action
from modules.handle_habits import habit_done
from modules.get_update import get_highscore, get_score_and_streak, get_habits
from modules.update_config import save_alarm_time, save_clockout_time
from modules.get_from_db import get_all_history
from modules.update_db import delete_row, update_today

from db_setup import setup_database
from config_setup import setup_config

# Create config, DB and table if they don't exist
setup_database()
setup_config()

app = Flask(__name__)

# Home route, renders the main page
@app.route('/')
def home():
    alarm_time = get_alarm_time()         # get alarm and clockout times from config to be rendered in frontend
    clockout_time = get_clockout_time()
    return render_template('index.html', alarm_time=alarm_time, clockout_time=clockout_time) 

# Called by AJAX (JS) to update streak and highscore without refreshing the page
@app.route('/update_highscore')
def update_highscore():
    highscore = get_highscore() # get current highscore to be sent to frontend
    return jsonify({
        "highscore": highscore
    })

@app.route('/update_score_and_streak')
def update_score_and_streak():
    score, streak = get_score_and_streak()
    return jsonify({
        "score": score,
        "streak": streak
    })

@app.route('/update_habits')
def update_habits():
    habit_values, habit_is_today = get_habits()
    return jsonify({
        "values": habit_values,
        "is_today": habit_is_today
    })

# Route to set a new alarm time, called by alarm edit form
@app.route('/set_alarm', methods=['POST'])
def set_alarm():
    if request.method == 'POST':
        new_alarm_time = request.form['alarm_time']
        save_alarm_time(new_alarm_time)
    
    return redirect(url_for('home'))

# Route to set a new clockout time, called by clockout edit form
@app.route('/set_clockout', methods=['POST'])
def set_clockout():
    if request.method == 'POST':
        new_clockout_time = request.form['clockout_time']
        save_clockout_time(new_clockout_time)

    return redirect(url_for('home'))

# Route called manually to clock out
@app.route('/clockout', methods=['GET'])
def clockout():
    clockout_action()
    return redirect(url_for('home'))

# Route called by the controller to stop the alarm
@app.route('/stop_alarm', methods=['POST'])
def stop_alarm():
    if request.method == 'POST':
        data = request.get_json() # get JSON data from request sent by controller
        if not data:
            return jsonify({"error": "No JSON received"}), 400

        # Extract fields
        time_str = data.get("time")
        seconds_str = data.get("seconds")

        print(f"Received time: {time_str}, seconds: {seconds_str}")
        stop_alarm_calc(time_str, seconds_str) # process the stop alarm request
    
    else:
        pass
    return "", 202 # ACCEPTED

# Route called by the controller to mark a habit as done
@app.route('/habit/<int:habit_id>', methods=['GET'])
def habit(habit_id):
    if habit_id not in {1, 2, 3, 4}:
        abort(404)
    habit_done(habit_id) # process the habit done request
    return "", 202 # ACCEPTED

@app.route('/history')
def history():
    rows = get_all_history()
    return render_template('history.html', rows=rows)

@app.route('/delete_id', methods=['POST'])
def delete_id():
    if request.method == 'POST':
        id = request.form['id']
        delete_row(id)
    return redirect(url_for('history'))

@app.route('/update_day', methods=['POST'])
def update_day():
    if request.method == 'POST':
        updateDate = request.form['date']
        column = request.form['column']
        updated = request.form['updated']

        data = {column: updated}

        update_today(date=updateDate, **data)
    return redirect(url_for('history'))

# Start the alarm watcher thread and run the Flask app
if __name__ == '__main__':
    threading.Thread(target=watch_alarm, daemon=True).start()
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)
