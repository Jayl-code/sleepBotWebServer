# Imports
import sqlite3
from datetime import date, timedelta

from modules.get_config import get_last_required_day

# File paths
db_file = 'database.db'

# Retrieves current streak, highscore, and score from the database to send to frontend
def get_update():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.execute("SELECT date, streak, score FROM history ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()

    cur.execute("SELECT score FROM history ORDER BY score DESC LIMIT 1")
    highscore = cur.fetchone()

    cur.close()
    conn.close()

    if highscore is None:
        return 0, 0, 0  # no data yet
    
    today = str(date.today())
    tomorrow = str(date.today() + timedelta(days=1))
    last_day_needed = get_last_required_day()
    
    if row[0] not in (today, tomorrow, last_day_needed): 
        return 0, highscore[0], 0
    
    return row[1], highscore[0], row[2]
