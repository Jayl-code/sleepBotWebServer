

# Imports
import sqlite3
import time
import logging

log = logging.getLogger(__name__)

# File paths
db_file = 'database.db'

def insert_history(**kwargs): # Call with (column name):(value) pairs to insert a new row. Must include date.
    date = kwargs.get("date")
    if not date: # Cannot insert without date
        log.exception("insert_history() called without date")
        raise ValueError("date is required for insert_history()")

    # Only use the keys that were passed in
    columns = ", ".join(kwargs.keys())
    placeholders = ", ".join(["?"] * len(kwargs))
    values = tuple(kwargs.values())

    # Make dynamic query
    query = f"""
        INSERT INTO history ({columns})
        VALUES ({placeholders})
    """

    # Retry logic
    for attempt in range(2):
        try:
            with sqlite3.connect(db_file, timeout=10) as conn:
                try:
                    cur = conn.cursor()
                    cur.execute(query, values) # Execute with dynamic values
                    conn.commit()
                    log.info(f"Inserted record for {date}")
                    return
                except Exception as e:
                    conn.rollback()
                    log.warning(f"Error inserting record for {date}: {e}")
        except sqlite3.OperationalError as e:
            if attempt == 1:  # Last attempt
                log.error(f"Failed to insert after 2 tries: {e}")
                raise
            log.warning(f"DB locked, retrying...")
            time.sleep(0.5)

    return

def update_today(**kwargs): # Call with date:(Date of row to update), (row to update):(New value)
    date = kwargs.get("date")
    if not date: # Cannot update without date
        log.exception("update_today() called without date")
        raise ValueError("date is required for update_today()")

    # Prepare dynamic SET clause
    set_parts = []
    values = []

    for key, value in kwargs.items():
        if key == "date":
            continue  # don't update this field
        set_parts.append(f"{key} = ?")
        values.append(value)

    # Nothing to update?
    if not set_parts:
        return

    set_clause = ", ".join(set_parts)
    values.append(date)  # add WHERE date value at the end

    query = f"""
        UPDATE history
        SET {set_clause}
        WHERE date = ?
    """

    # Retry logic
    for attempt in range(2):
        try:
            with sqlite3.connect(db_file, timeout=10) as conn:
                try:
                    cur = conn.cursor()
                    cur.execute(query, tuple(values)) # Execute with dynamic values
                    conn.commit()
                    log.info(f"Updated record for {date}")
                    return
                except Exception as e:
                    conn.rollback()
                    log.warning(f"Error updating record for {date}: {e}")
        except sqlite3.OperationalError as e:
            if attempt == 1:  # Last attempt
                log.error(f"Failed to update after 2 tries: {e}")
                raise
            log.warning(f"DB locked, retrying...")
            time.sleep(0.5)

    return

def delete_row(id): # Call with the id of the row to delete
    # Retry logic
    for attempt in range(2):
        try:
            with sqlite3.connect(db_file, timeout=10) as conn:
                try:
                    cur = conn.cursor()
                    cur.execute("DELETE FROM history WHERE id = ?", (id,)) # Delete by id
                    conn.commit()
                    log.info(f"Deleted record with id {id}")
                    return
                except Exception as e:
                    conn.rollback()
                    log.warning(f"Error deleting record with id {id}: {e}")
        except sqlite3.OperationalError as e:
            if attempt == 1:  # Last attempt
                log.error(f"Failed to delete after 2 tries: {e}")
                raise
            log.warning(f"DB locked, retrying...")
            time.sleep(0.5)

    return