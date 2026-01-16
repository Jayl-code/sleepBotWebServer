# Imports
from datetime import date

from modules.get_config import get_last_required_day
from modules.get_from_db import get_dates_history


# Retrieves current streak, highscore, and score from the database to send to frontend

def get_current_score():
    today = str(date.today())
    todays_score = get_dates_history(today, ["score"])
    if not todays_score:
        return 0
    return todays_score[0]

def get_current_streak():
    today = str(date.today())
    today_history = get_dates_history(today, ["streak"])
    if not today_history:
        last_streak = get_dates_history(get_last_required_day(), ["streak"])
        if not last_streak:
            return False, 0
        else:
            return False, last_streak[0]

    return True, today_history[0]

def get_current_habits():
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
        
    return habit_is_today, habit_values