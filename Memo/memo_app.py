from functools import partial
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import sqlite3
# import datetime
# from datetime import date
from datetime import datetime

root = Tk()  # creating the GUI window

root.title('Memo app')
#root.geometry("600x600")

canvas = Canvas(root, width=600, height=300)
canvas.grid(columnspan=3)

#logo
logo= Image.open('logo.jpg')
logo = ImageTk.PhotoImage(logo)
logo_label = Label(image=logo)
logo_label.image = logo
logo_label.grid(column=1, row=0)

# Database:

# Create the database/ Connect to a DB
conn = sqlite3.connect('saved_memos.db')

# create a cursor:
c = conn.cursor()

# Creating the table:
c.execute("""CREATE TABLE if not exists memos (
        date text,
        time text,
        content txt
        )""")

c.execute("SELECT *, oid FROM memos")
records = c.fetchall()

#Function to update a Memo
def update():
    return

# Function to ope an existing memo
def open_memo(id):
    print(id)
    global editor, date, time
    editor = Tk()  # creating the GUI window
    editor.title('Update a record')
    editor.geometry("600x300")

    conn = sqlite3.connect('saved_memos.db')
    c = conn.cursor()

    record_id = str(id)
    c.execute("SELECT * FROM memos WHERE oid = " + record_id)
    records = c.fetchall()

    #Creating Global Variables for text box names
    global date_edit
    global time_edit
    global content_edit

    content_edit = Text(editor, height=10, width=30)
    content_edit.grid(row=2, column=1)

    for record in records:
        date = record[0]
        time = record[1]

    # Creating the text box Labels
    date_label = Label(editor, text=date)
    date_label.grid(row=0, column=1)
    time_label = Label(editor, text="Last edited at:  " + time)
    time_label.grid(row=1, column=1)
    content_label = Label(editor, text="Memo Content:")
    content_label.grid(row=2, column=0)

    # Create a save button:
    save_btn = Button(editor, text="Save", command=update)
    save_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=135)

    # Loop through the results:
    for record in records:
        content_edit.insert('1.0', record[2])

    conn.commit()
    conn.close()


def show():
    conn = sqlite3.connect('saved_memos.db')
    c = conn.cursor()

    # Query the db
    c.execute("SELECT *, oid FROM memos")
    records = c.fetchall()

    print_rec = ''
    for record in records:
        print_rec += str(record[0]) + " " + str(record[1]) + " " + str(record[2]) + " " + str(record[3]) + "\n"

    query_label = Label(root, text=print_rec)
    query_label.grid(row=2, column=0, columnspan=2)

    conn.commit()
    conn.close()


#Showing all the existing notes
count=2
for record in records:
    current_rec = str(record[3]) + " " + str(record[0]) + " " + str(record[2]).split()[0] + "\n"
    current_id = record[3]
    query_btn = Button(root, text=current_rec, height=2, width=100, command=partial(open_memo, current_id))
    query_btn.grid(row=count, column=0, columnspan=3, pady=10, padx=10)
    count += 1

# query_btn1 = Button(root, text="shit", height=2, width=100, command=open)
# query_btn1.grid(row=count, column=0, columnspan=3, pady=10, padx=10)
#command=lambda: open(i)



# Create a New memo button
new_btn = Button(root, text="Create new Memo", command= show)
new_btn.grid(row=count+1, column=2, columnspan=1, pady=10, padx=10)

root.mainloop()
