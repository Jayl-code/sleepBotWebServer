# Imports
from flask import Flask, render_template, redirect, url_for, request, jsonify, abort 
import threading

from modules import *
from dbsetup import setup_database

# Create DB and table if it doesn't exist
setup_database()

app = Flask(__name__)

# Home route, renders the main page
@app.route('/')
def home():
    alarm_time, clockout_time = get_config() # get alarm and clockout times from config to be rendered in frontend
    # history = get_history() // todo: add history display in frontend and 'history=history' in render_template
    return render_template('index.html', alarm_time=alarm_time, clockout_time=clockout_time,) 

# Called by AJAX (JS) to update streak and highscore without refreshing the page
@app.route('/update_data')
def update_data():
    streak, highscore, current_score = get_update() # get current streak, highscore, and score to be sent to frontend
    return jsonify({
        "streak": streak,
        "highscore": highscore,
        "current_score": current_score
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

# Start the alarm watcher thread and run the Flask app
if __name__ == '__main__':
    threading.Thread(target=watch_alarm, daemon=True).start()
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)
