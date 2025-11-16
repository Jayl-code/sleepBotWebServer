from flask import Flask, render_template, redirect, url_for, request, jsonify, abort 
from modules import *
import threading

app = Flask(__name__)

@app.route('/')
def home():
    alarm_time, clockout_time = get_config()
    history = get_history()
    return render_template('index.html', alarm_time=alarm_time, clockout_time=clockout_time, history=history)

# Called by AJAX (JS) to update streak and highscore without refreshing the page
@app.route('/update_data')
def update_data():
    return jsonify({
        "streak": get_streak(),
        "highscore": get_highscore(),
        "current_score": get_current_score()
        })

@app.route('/set_alarm', methods=['POST'])
def set_alarm():
    if request.method == 'POST':
        new_alarm_time = request.form['alarm_time']
        save_alarm_time(new_alarm_time)
    
    return redirect(url_for('home'))

@app.route('/set_clockout', methods=['POST'])
def set_clockout():
    if request.method == 'POST':
        new_clockout_time = request.form['clockout_time']
        save_clockout_time(new_clockout_time)

    return redirect(url_for('home'))

@app.route('/stop_alarm', methods=['POST'])
def stop_alarm():
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON received"}), 400

        # Extract fields
        time_str = data.get("time")
        seconds_str = data.get("seconds")

        print(f"Received time: {time_str}, seconds: {seconds_str}")
        stop_alarm_calc(time_str, seconds_str)
    
    else:
        pass
    return redirect(url_for('home'))

# Called by the controller when a habit button is clicked
@app.route('/habit/<int:habit_id>', methods=['GET'])
def habit(habit_id):
    if habit_id not in {1, 2, 3, 4}:
        abort(404)
    habit_done(habit_id)
    return redirect(url_for('home'))

if __name__ == '__main__':
    threading.Thread(target=watch_alarm, daemon=True).start()
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)
