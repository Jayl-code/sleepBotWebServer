# Imports
import sqlite3

# File paths
db_file = 'database.db'
    
def get_last_history():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.execute("SELECT date, id, streak, clockout, alarmAttempted FROM history ORDER BY id DESC LIMIT 1")
    row = cur.fetchone() # get previous date and the id of it

    cur.close()
    conn.close()

    return row