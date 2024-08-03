import sqlite3
import tkinter as tk

conn = sqlite3.connect("Entry")
cursor = conn.cursor()

conn.execute('''
    CREATE TABLE IF NOT EXISTS Journal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Entry TEXT NOT NULL,
        Ratings TEXT NOT NULL     
    )
''')


