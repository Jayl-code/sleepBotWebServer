# Imports
import sqlite3
import time
import logging

log = logging.getLogger(__name__)

# File paths
db_file = 'database.db'


def get_dates_history(date, columns): # Input date then a list of the things to get eg. get_dates_history(date, ["streak", "score"])
    if not columns:
        log.exception("get_dates_history() called without columns")
        raise ValueError("At least one column must be specified.")

    # Make column list
    col_clause = ", ".join(columns)

    query = f"""
        SELECT {col_clause} FROM history WHERE date = ? LIMIT 1
        """

    # Retry logic
    for attempt in range(2):
        try:
            with sqlite3.connect(db_file, timeout=10) as conn:
                try:
                    cur = conn.cursor()
                    cur.execute(query, (date,)) # Execute with dynamic values
                    row = cur.fetchone()
                    return row
                except Exception as e:
                    log.warning(f"Error retrieving record for {date}: {e}")
                    raise
        except sqlite3.OperationalError as e:
            if attempt == 1:  # Last attempt
                log.error(f"Failed to retrieve after 2 tries: {e}")
                raise
            log.warning(f"DB locked, retrying...")
            time.sleep(0.5)

    return

def get_current_highscore():
    # Retry logic
    for attempt in range(2):
        try:
            with sqlite3.connect(db_file, timeout=10) as conn:
                try:
                    cur = conn.cursor()
                    cur.execute("SELECT score FROM history ORDER BY score DESC LIMIT 1")
                    highscore = cur.fetchone()
                    if highscore is None:
                        return 0 
                    return highscore[0]
                except Exception as e:
                    log.warning(f"Error retrieving highscore: {e}")
                    raise
        except sqlite3.OperationalError as e:
            if attempt == 1:  # Last attempt
                log.error(f"Failed to retrieve highscore after 2 tries: {e}")
                raise
            log.warning(f"DB locked, retrying...")
            time.sleep(0.5)

    return

def get_all_history():
    # Retry logic
    for attempt in range(2):
        try:
            with sqlite3.connect(db_file, timeout=10) as conn:
                try:
                    conn.row_factory = sqlite3.Row 
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM history")
                    rows = cur.fetchall()
                    return rows
                except Exception as e:
                    log.warning(f"Error retrieving all history: {e}")
                    raise
        except sqlite3.OperationalError as e:
            if attempt == 1:  # Last attempt
                log.error(f"Failed to retrieve all history after 2 tries: {e}")
                raise
            log.warning(f"DB locked, retrying...")
            time.sleep(0.5)

    return
