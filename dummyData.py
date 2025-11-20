import sqlite3

dummy_data = [
    # id will autoincrement, so no need to provide
    {
        "date": "2025-11-18",
        "clockout": 1,
        "alarmStopped": 0,
        "stopTime": 1600,
        "habit1": 1,
        "habit2": 0,
        "habit3": 1,
        "habit4": 0,
        "streak": 3,
        "score": 90
    },
    {
        "date": "2025-11-19",
        "clockout": 0,
        "alarmStopped": 1,
        "stopTime": 1550,
        "habit1": 1,
        "habit2": 1,
        "habit3": 1,
        "habit4": 0,
        "streak": 4,
        "score": 60
    },
    {
        "date": "2025-11-20",
        "clockout": 1,
        "alarmStopped": 1,
        "stopTime": 1500,
        "habit1": 1,
        "habit2": 1,
        "habit3": 1,
        "habit4": 1,
        "streak": 5,
        "score": 70
    },
]

def insert_dummy_data():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    for row in dummy_data:
        cur.execute("""
            INSERT INTO history (date, clockout, alarmStopped, stopTime, habit1, habit2, habit3, habit4, streak, score)
            VALUES (:date, :clockout, :alarmStopped, :stopTime, :habit1, :habit2, :habit3, :habit4, :streak, :score)
        """, row)

    conn.commit()

    cur.close()
    conn.close()

def clear_history():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM history")
    cur.execute("DELETE FROM sqlite_sequence WHERE name='history'")
    conn.commit()
    cur.close()
    conn.close()

#clear_history()
#insert_dummy_data()