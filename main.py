import tkinter as tk
from tkinter import ttk
import sqlite3
import database



class Page:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MainPage")
        self.root.resizable(False, False)

    def MainView(self):
        self.leftFrame = tk.Frame(self.root, width=200, height=300, bg="lightgray")
        self.leftFrame.grid(columnspan=2, row=0, sticky="ns") 

        tk.Button(self.leftFrame, text="New Entry", command="").grid(column=0,row=0, padx=5, pady=5, sticky="ew")
        tk.Button(self.leftFrame, text="View All", command="").grid(column=0,row=1, padx=5, pady=5, sticky="ew")
        tk.Button(self.leftFrame, text="Delete", command=self.Delete).grid(column=0,row=2, padx=5, pady=5, sticky="ew")

        
        self.treeView = ttk.Treeview(self.root, columns=("Entry Field", "Overall Rating"))
        self.treeView.heading("#0", text="Name")  
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
    
    def Delete(self):
        selectedItem = self.treeView.selection()

        
        item = selectedItem[0]

        bookAuthor = self.treeView.item(item, "text")
        bookName = self.treeView.item(item, "values")[0]
        PublishDate = self.treeView.item(item, "values")[1]

        self.treeView.delete(item)
        self.cursor.execute("DELETE FROM Journal WHERE Name = ? AND Entry = ? And Ratings = ?", (bookAuthor, bookName, PublishDate))
        self.conn.commit()


    def NewEntry():
        pass
    
    def ViewAll():
        pass
    
Page().MainView()