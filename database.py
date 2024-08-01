import sqlite3


conn = sqlite3.connect("Entry")
conn.execute('''
    CREATE TABLE IF NOT EXISTS Journal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Entry TEXT NOT NULL,
        Ratings TEXT NOT NULL     
    )
''')