# Imports
import sqlite3

# File paths
db_file = 'database.db'

# Retrieves current streak, highscore, and score from the database to send to frontend
def get_update():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.execute("SELECT streak FROM history ORDER BY id DESC LIMIT 1")
    streak = cur.fetchone()

    cur.execute("SELECT score FROM history ORDER BY score DESC LIMIT 1")
    highscore = cur.fetchone()

    cur.execute("SELECT score FROM history ORDER BY id DESC LIMIT 1")
    score = cur.fetchone()
    
    cur.close()
    conn.close()
    if streak is None:
        return 0, 0, 0  # no data yet
    return streak[0], highscore[0], score[0]

#todo rewrite to be better and handle no data case and if the streak has ran out