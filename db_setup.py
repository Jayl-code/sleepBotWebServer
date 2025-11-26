import sqlite3

def setup_database():
    # Connect to SQLite database (or create it if it doesn't yet exist)
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Create history table if it doesn't exist
    cur.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT UNIQUE,
        clockout INTEGER DEFAULT 0 CHECK(clockout IN (0, 1)),
        alarmStopped INTEGER DEFAULT 0 CHECK(alarmStopped IN (0, 1)),
        stopTime INTEGER,
        habit1 INTEGER DEFAULT 0 CHECK(habit1 IN (0, 1)),
        habit2 INTEGER DEFAULT 0 CHECK(habit2 IN (0, 1)),
        habit3 INTEGER DEFAULT 0 CHECK(habit3 IN (0, 1)),
        habit4 INTEGER DEFAULT 0 CHECK(habit4 IN (0, 1)),
        streak INTEGER DEFAULT 0,
        score INTEGER DEFAULT 0
        )
    """)


    conn.commit()

    cur.close()
    conn.close()

    return