import tkinter as tk
from tkinter import ttk
import sqlite3




class Page:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MainPage")
        self.root.resizable(False, False)

    def MainView(self):
        self.leftFrame = tk.Frame(self.root, width=200, height=300, bg="lightgray")
        self.leftFrame.grid(columnspan=2, row=0, sticky="ns") 

        tk.Button(self.leftFrame, text="New Entry", command=self.NewEntry).grid(column=0,row=0, padx=5, pady=5, sticky="ew")
        tk.Button(self.leftFrame, text="View All", command="").grid(column=0,row=1, padx=5, pady=5, sticky="ew")
        tk.Button(self.leftFrame, text="Delete", command=self.Delete).grid(column=0,row=2, padx=5, pady=5, sticky="ew")
        #tk.Button(self.leftFrame, text="Refresh", command=self.Refresh).grid(column=0,row=2, padx=5, pady=5, sticky="ew")

        
        self.treeView = ttk.Treeview(self.root, columns=("Entry Field", "Overall Rating"))
        self.treeView.heading("#0", text="Name")  
        self.treeView.heading("Entry Field", text="Entry Field")
        self.treeView.heading("Overall Rating", text="Overall Rating")
        
        self.treeView.tag_configure('separator', background="lightblue")

        self.treeView.grid(column=3, row=0, sticky="nsew")

        self.conn = sqlite3.connect("Entry")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM Journal")
        
        results = self.cursor.fetchall()

        for row in results:
            self.treeView.insert("", tk.END, text=row[1], values=(row[2], row[3]))
        
        self.cursor.execute("SELECT COUNT (*) FROM Journal")
        self.count = self.cursor.fetchone()
        tk.Label(self.leftFrame, text=self.count).grid(columnspan=2, row=4, sticky="ew")


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


    def NewEntry(self):
        self.new = tk.Tk()
        self.new.config(bg="lightblue")
        self.new.title("Entry's")
        self.new.geometry("300x300")
        self.new.resizable(False, False)
        

        
        tk.Label(self.new, text="Name", bg="Lightblue").grid(column=0, row=0, padx=2, pady=2, sticky="w")
        self.ent1 = tk.Entry(self.new, width=30)
        self.ent1.grid(column=1, row=0,padx=2, pady=2, sticky="ew")
        
        tk.Label(self.new, text="Entry", bg="Lightblue").grid(column=0, row=2, padx=2, pady=2, sticky="w")
        self.ent2 = tk.Text(self.new, width=30, height=8)
        self.ent2.grid(column=1, row=2,padx=2, pady=2, sticky="ew")

        
        tk.Label(self.new, text="Rating", bg="Lightblue").grid(column=0, row=4, padx=2, pady=2, sticky="w")
        self.ent3 = tk.Text(self.new, width=30, height=4)
        self.ent3.grid(column=1, row=4,padx=2, pady=2, sticky="ew")

        tk.Button(self.new, text="Submit", bg="white", command=self.New).grid(column=1, row=5, padx=2, pady=5, sticky="ew")
        tk.Button(self.new, text="Cancel", bg="White", command=self.cancel).grid(column=1, row=6, padx=2, pady=5, sticky="ew")
        

        self.new.mainloop()

    
    def cancel(self):
        self.new.destroy()
    
    def New(self):
        
        Name = self.ent1.get().strip()
        Entry = self.ent2.get("1.0", "end-1c").strip()
        Rating = self.ent3.get("1.0", "end-1c").strip()

        if Name and Entry and Rating:
            self.cursor.execute("INSERT INTO Journal(Name, Entry, Ratings) VALUES (?, ?, ?)", (Name, Entry, Rating))
            self.conn.commit()
            self.treeView.insert("", tk.END, text=Name, values=(Entry, Rating))
            self.new.destroy()
        else:
            print("please fill in all the fields")
        
        def ViewAll():
            pass
    
Page().MainView()