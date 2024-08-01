import tkinter as tk
from tkinter import ttk
import sqlite3
import database

conn = sqlite3.connect("Entry")
conn.execute('''
    CREATE TABLE IF NOT EXISTS Journal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Entry TEXT NOT NULL,
        Ratings TEXT NOT NULL     
    )
''')


class Page:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MainPage")
        self.root.resizable(False, False)

    def MainView(self):
        self.leftFrame = tk.Frame(self.root, width=200, height=300, bg="lightgray")
        self.leftFrame.grid(columnspan=2, row=0, sticky="ns") 

        # Create a Treeview widget with columns "Name" and "Entry Field"
        self.treeView = ttk.Treeview(self.root, columns=("Entry Field", "Overall Rating"))
        
        # Setup headings
        self.treeView.heading("#0", text="Name")  # "#0" is the default column for the tree item label
        self.treeView.heading("Entry Field", text="Entry Field")
        self.treeView.heading("Overall Rating", text="Overall Rating")
        

 
        self.treeView.grid(column=3, row=0, sticky="nsew")

        self.conn = sqlite3.connect("Entry")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM Journal")
        results = self.cursor.fetchall()

        for row in results:
            self.treeView.insert("", tk.END, text=row[1], values=(row[2], row[3]))
        
        
    



        self.root.mainloop()


    
Page().MainView()