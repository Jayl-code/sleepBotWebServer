# Imports
from datetime import date, timedelta

from modules.get_config import get_last_required_day
from modules.get_from_db import get_dates_history, get_current_highscore

# File paths
db_file = 'database.db'

# Retrieves current streak, highscore, and score from the database to send to frontend
def get_highscore():
    highscore = get_current_highscore() 
    if highscore is None:
        return 0 
    return highscore

def get_score_and_streak():
    today = str(date.today())
    today_history = get_dates_history(today, ["score", "streak"])
    if not today_history:
        last_streak = get_dates_history(get_last_required_day(), ["streak"])
        if not last_streak:
            return 0, 0
        else:
            return 0, last_streak[0]
        
    return today_history[0], today_history[1]

def get_habits():
    habits = ["habit1", "habit2", "habit3", "habit4"]
    today = str(date.today())
    last_habits = get_dates_history(get_last_required_day(), habits)
    todays_habits = get_dates_history(today, habits)

    # If they returned None, replace with zero-filled lists
    if last_habits is None:
        last_habits = [0] * len(habits)

    if todays_habits is None:
        todays_habits = [0] * len(habits)

    habit_values = {}
    habit_is_today = {}

    for i, h in enumerate(habits):
        if todays_habits[i] != 0:
            habit_values[h] = todays_habits[i]
            habit_is_today[h] = True
        else:
            habit_values[h] = last_habits[i]
            habit_is_today[h] = False
        
    return habit_values, habit_is_today