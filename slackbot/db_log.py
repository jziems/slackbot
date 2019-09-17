import sqlite3

conn = sqlite3.connect('facedata.db')

def create_db():
    global conn

    conn.execute('''CREATE TABLE IF NOT EXISTS MESSAGES (ID INTEGER PRIMARY KEY ASC, client_msg_id: TEXT NOT NULL, suppress_notification: INTEGER NOT NULL, text: TEXT NOT NULL, user: TEXT NOT NULL, team: TEXT NOT NULL, user_team: TEXT NOT NULL, source_team: TEXT NOT NULL, channel: TEXT NOT NULL, event_ts: INTEGER NOT NULL, ts: INTEGER NOT NULL);''')
    conn.commit()

def insert_entry():
    global conn

    conn.commit()
