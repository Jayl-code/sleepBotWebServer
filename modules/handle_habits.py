from datetime import date
import logging

log = logging.getLogger(__name__)

from modules.get_from_db import get_dates_history
from modules.get_config import get_last_required_day
from modules.update_db import update_today
from modules.handle_sounds import play_sound_effect


def habit_done(habit_id):

    dateToday = str(date.today())

    try:
        todays_history = get_dates_history(dateToday, ["habit1", "habit2", "habit3", "habit4", "score"])
        last_history = get_dates_history(get_last_required_day(), ["habit1", "habit2", "habit3", "habit4"])
    except Exception:
        log.exception("Failed to retrieve habit data from database")
        return

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

        _which_sound_effect(todays_history, index, new_streak)

        update_today(
            date=dateToday,
            score=new_score,
            **{habit_name: new_streak}
        )
        log.info(f"Habit {habit_id} completed. Habit streak: {new_streak}, Score increased by {bonus}.")

def _which_sound_effect(todays_history, habit_index, new_streak):
    updated_habits = list(todays_history[:4])
    updated_habits[habit_index] = new_streak

    if all(habit > 0 for habit in updated_habits):
        play_sound_effect("habits_complete")
        log.info("All habits complete sound played.")
    else:
        play_sound_effect("habit")
        log.info("Single habit complete sound played.")