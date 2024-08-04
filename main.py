import tkinter as tk
from tkinter import ttk
import sqlite3

class Page:


    def MainView(self):
        self.root = tk.Tk()
        self.root.title("MainPage")
        self.root.resizable(False, False)


        self.style = ttk.Style()

        self.style.theme_use("clam")

        self.style.configure("Treeview", 
                             background = "lightgrey",
                             foreground = "black",
                             rowheight=20,
                             fieldbackground = "lightgrey")
        
        self.style.map("Treeview", 
                       background=[("selected", "black")])
        

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
        

        self.leftFrame = tk.Frame(self.root, width=200, height=300, bg="lightgray")
        self.leftFrame.grid(columnspan=2, row=0, sticky="ns") 

        tk.Button(self.leftFrame, text="New Entry", bg="lightgrey",activebackground="black", activeforeground="white", command=self.NewEntry).grid(column=0,row=0, padx=5, pady=5, sticky="ew")
        tk.Button(self.leftFrame, text="View All", bg="lightgrey",activebackground="black", activeforeground="white", command=self.ViewAll).grid(column=0,row=1, padx=5, pady=5, sticky="ew")
        tk.Button(self.leftFrame, text="Delete", bg="lightgrey",activebackground="black", activeforeground="white", command=self.Delete).grid(column=0,row=2, padx=5, pady=5, sticky="ew")
        tk.Button(self.leftFrame, text="expand",  bg="lightgrey",activebackground="black", activeforeground="white",command=self.Expand).grid(column=0,row=3, padx=5, pady=5, sticky="ew")
        tk.Button(self.leftFrame, text="Refresh",  bg="lightgrey",activebackground="black", activeforeground="white",command=self.Refresh).grid(column=0,row=4, padx=5, pady=5, sticky="ew")

        
        self.cursor.execute("SELECT COUNT (*) FROM Journal")
        self.count = self.cursor.fetchone()
        tk.Label(self.leftFrame, text=self.count).grid(columnspan=2, row=5, sticky="ew")


        self.root.mainloop()
    
    def Expand(self):
        selectedItem = self.treeView.selection()


        if selectedItem:
            item = self.treeView.item(selectedItem)
            itemName = item['text']
            itemValues = item['values']

            
            FullEntry = tk.Toplevel(self.root)
            FullEntry.title("Journal Entry")
            FullEntry.resizable(False, False)

            
        

            tk.Label(FullEntry, text=f"Name: {itemName}").grid(row=0, column=0, padx=5, pady=5)
            tk.Label(FullEntry, text=f"Entry Field: {itemValues[0]}").grid(row=1, column=0, padx=5, pady=5)
            tk.Label(FullEntry, text=f"Overall Rating: {itemValues[1]}").grid(row=2, column=0, padx=5, pady=5)


    def Refresh(self):
        self.root.destroy()
        self.MainView()
    

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
        
    def ViewAll(self):
        self.root.destroy()

        self.view = tk.Tk()
        self.view.config(bg="Lightgrey")
        self.view.title("Database Entries")

        self.style = ttk.Style()

        self.style.theme_use("clam")

        self.style.configure("Treeview", 
                             background = "lightgrey",
                             foreground = "black",
                             rowheight=20,
                             fieldbackground = "lightgrey")
        
        self.style.map("Treeview", 
                       background=[("selected", "black")])
        


        self.treeView = ttk.Treeview(self.view, columns=("Entry Field", "Overall Rating"))
        self.treeView.heading("#0", text="Name")  
        self.treeView.heading("Entry Field", text="Entry Field")
        self.treeView.heading("Overall Rating", text="Overall Rating")
        self.treeView.grid(column=3, row=0, sticky="nsew")

        maxShowing = 25
        self.treeView.configure(height=maxShowing)

        self.conn = sqlite3.connect("Entry")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM Journal")
        
        results = self.cursor.fetchall()
        
        for row in results:
            self.treeView.insert("", tk.END, text=row[1], values=(row[2], row[3]))

        tk.Button(self.view, text="Return", bg="lightgrey",activebackground="black", activeforeground="white", command=self.cancel).grid(column=0, row=0, sticky="ns")

    def cancel(self):
        self.view.destroy()
        self.MainView()




    
Page().MainView()