import sqlite3

def save_response_to_db(id_,user_name_, user_, assistant_, timestamp_):
    """
    Save the response and user to the database.
    """
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS responses (id TEXT, user_name TEXT, user TEXT, assistant TEXT, timestamp TEXT)")
    c.execute("INSERT INTO responses (id, user_name, user, assistant, timestamp) VALUES (?, ?, ?, ?, ?)",
              (id_, user_name_, user_, assistant_, timestamp_))
    
    conn.commit()
    conn.close()