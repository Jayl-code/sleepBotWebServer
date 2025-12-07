# Imports
import sqlite3

# File paths
db_file = 'database.db'

def insert_history(**kwargs):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    # Cannot insert without date
    date = kwargs.get("date")
    if not date:
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

    cur.execute(query, values)
    conn.commit()

    cur.close()
    conn.close()

    return

def update_today(**kwargs): # Call with date:(Date of row to update), (row to update):(New value)
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    # Cannot update without date
    date = kwargs.get("date")
    if not date:
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
        cur.close()
        conn.close()
        return

    set_clause = ", ".join(set_parts)
    values.append(date)  # add WHERE date value at the end

    query = f"""
        UPDATE history
        SET {set_clause}
        WHERE date = ?
    """

    cur.execute(query, tuple(values))
    conn.commit()

    cur.close()
    conn.close()

    return

def delete_row(id):

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM history WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return