# Imports
import sqlite3

# File paths
db_file = 'database.db'

def insert_history(**kwargs):
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()

        cur.execute("""
                INSERT INTO history 
                (date, clockout, alarmStopped, stopTime, streak, score, alarmAttempted)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                kwargs.get("date"),
                kwargs.get("clockout", 0),
                kwargs.get("alarmStopped", 0),
                kwargs.get("stopTime", 0),
                kwargs.get("streak", 0),
                kwargs.get("score", 0),
                kwargs.get("alarmAttempted", 0)
            ))
        conn.commit()

        cur.close()
        conn.close()

        return

def update_today(**kwargs):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.execute("""
                UPDATE history
                SET alarmStopped = ?, stopTime = ?, score = ?, streak = ?, alarmAttempted = ?
                WHERE date = ?
            """, (
                kwargs.get("alarmStopped", 0),
                kwargs.get("stopTime", 0),
                kwargs.get("score", 0),
                kwargs.get("streak", 0),
                kwargs.get("alarmAttempted", 0),
                kwargs.get("dateToday")
            ))
    
    conn.commit()

    cur.close()
    conn.close()

    return