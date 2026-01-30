# db_setup.py

# Imports
import sqlite3
import time
import sys
import logging

log = logging.getLogger(__name__)

def setup_database():
    # Connect to SQLite database (or create it if it doesn't yet exist)
    # Retry logic
    log.info("Setting up database...")
    for attempt in range(2):
        try:
            with sqlite3.connect('database.db', timeout=10) as conn:
                try:
                    cur = conn.cursor()
                    # If the table already exists, report and return
                    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='history'")
                    if cur.fetchone():
                        log.info("Database already set up.")
                        return

                    # Create history table (it doesn't exist yet)
                    cur.execute("""
                    CREATE TABLE IF NOT EXISTS history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT UNIQUE NOT NULL,
                        clockout INTEGER DEFAULT 0 CHECK(clockout IN (0, 1)),
                        alarmStopped INTEGER DEFAULT 0 CHECK(alarmStopped IN (0, 1)),
                        stopTime INTEGER,
                        habit1 INTEGER DEFAULT 0,
                        habit2 INTEGER DEFAULT 0,
                        habit3 INTEGER DEFAULT 0,
                        habit4 INTEGER DEFAULT 0,
                        streak INTEGER DEFAULT 0,
                        score INTEGER DEFAULT 0,
                        alarmAttempted INTEGER DEFAULT 0 CHECK(alarmAttempted IN (0, 1))
                        )
                    """)
                    conn.commit()
                    log.info("Database setup completed successfully.")
                    return
                except Exception as e:
                    conn.rollback()
                    log.warning(f"Error setting up database: {e}")
        except sqlite3.OperationalError as e:
            if attempt == 1:  # Last attempt
                log.error(f"Failed to set up database after 2 tries: {e}")
                sys.exit(1)
            log.warning(f"DB locked, retrying...")
            time.sleep(0.5)

    return