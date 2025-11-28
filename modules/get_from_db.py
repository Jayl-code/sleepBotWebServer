from datetime import datetime, date, timedelta
import sqlite3

db_file = 'database.db'

def get_current_streak():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.execute("SELECT streak, date FROM history ORDER BY id DESC LIMIT 1")
    row = cur.fetchone() # get previous streak

    cur.close()
    conn.close()

    if row is None or row[1] != str(date.today() - timedelta(days=1)):
        return 0  # no previous entries or not consecutive day
    else:
        return row[0]