# Imports
import sqlite3

# File paths
db_file = 'database.db'


def get_dates_history(date, columns): # Input date then a list of the things to get eg. get_dates_history(date, ["streak", "score"])
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    if not columns:
        raise ValueError("At least one column must be specified.")

    # Make column list
    col_clause = ", ".join(columns)

    query = f"""
        SELECT {col_clause} FROM history WHERE date = ? LIMIT 1
        """

    cur.execute(query, (date,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    return row
