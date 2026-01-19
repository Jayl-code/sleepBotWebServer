from datetime import date
import logging

from modules.get_from_db import get_dates_history
from modules.get_config import get_last_required_day
from modules.update_db import update_today

log = logging.getLogger(__name__)

def habit_done(habit_id):

    dateToday = str(date.today())
    todays_history = get_dates_history(dateToday, ["habit1", "habit2", "habit3", "habit4", "score"])
    last_history = get_dates_history(get_last_required_day(), ["habit1", "habit2", "habit3", "habit4"])

    if not todays_history:
        log.info("Day not yet in database")
        return

    # If no previous day exists, treat all streaks as 0
    if not last_history:
        last_history = [0, 0, 0, 0]

    index = habit_id - 1  # convert habit_id 1 to 0, 2 to 1, etc.
    habit_name = f"habit{habit_id}"

    # Check if today's habit is still incomplete
    if todays_history[index] == 0:
        previous_streak = int(last_history[index])
        new_streak = previous_streak + 1

        bonus = int(20 * (1 + previous_streak / 10))
        new_score = int(todays_history[4]) + bonus

        update_today(
            date=dateToday,
            score=new_score,
            **{habit_name: new_streak}
        )
        log.info(f"Habit {habit_id} completed. Habit streak: {new_streak}, Score increased by {bonus}.")