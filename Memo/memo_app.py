from functools import partial
from tkinter import *
import tkinter as tk
from tkinter import ttk

from PIL import ImageTk, Image
import sqlite3
# import datetime
# from datetime import date
from datetime import datetime

root = Tk()  # creating the GUI window

root.title('Memo app')
root.geometry("750x900")
root.configure(background='white', border=0)

# logo
logo = Image.open('logo.jpg')
logo = ImageTk.PhotoImage(logo)
logo_label = Label(image=logo, border=0)
logo_label.image = logo
logo_label.pack()

# Create a main frame:
main_frame = Frame(root, border=0)
main_frame.pack(fill=BOTH, expand=1)

canvas = Canvas(main_frame, background='white', border=0)
# canvas.grid(columnspan=3)
canvas.pack(side=LEFT, fill=BOTH, expand=1)

# Add a scrollbar
my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

# Configure the canvas
canvas.configure(yscrollcommand=my_scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create another frame
second_frame = Frame(canvas, background='white', border=0)

# Adding a new window to the Canvas:
canvas.create_window((0, 0), window=second_frame, anchor="nw")

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


def hide_used_btns():
    for widget in second_frame.winfo_children():
        widget.destroy()


# Deleting an element from the DB
def delete(id):
    conn = sqlite3.connect('saved_memos.db')
    c = conn.cursor()

    # Delete a record:
    c.execute("DELETE from memos WHERE oid = " + id)

    conn.commit()
    conn.close()
    hide_used_btns()
    update_main_screen()
    editor.destroy()


# Adding a new memo to the DB
def save():
    conn = sqlite3.connect('saved_memos.db')
    c = conn.cursor()

    # Insert into table:
    c.execute("INSERT INTO memos VALUES (:date, :time, :content)",
              {
                  # python dictionary
                  'date': datetime.today().strftime('%Y-%m-%d'),
                  'time': datetime.today().strftime('%H:%M:%S'),
                  'content': content.get("1.0", "end")
              })

    conn.commit()
    conn.close()
    update_main_screen()
    new_memo.destroy()

def add_elem():
    global list_count
    content.insert('1.0', add_list.get()+"\n")
    add_list.delete(0, END)


# Creating a new Memo
def new_memo():
    global new_memo, content, add_list
    new_memo = Tk()
    new_memo.title('Create a new memo')
    new_memo.geometry("750x900")
    new_memo.rowconfigure(3)
    new_memo.configure(background='white', border=0)


    #Adding elements to a list
    list_label = Label(new_memo, text="Add new element to the list: ", border=0, font="Rockwell 13 bold", bg='white')
    list_label.grid(row=0, column=1)
    add_list = Entry(new_memo, width=10)
    add_list.grid(row=1, column=1,columnspan=2, pady=10, ipadx=145)

    add_btn = Button(new_memo, text="Add", width=5, height=1,bg='#fcd190', border=0, font="Rockwell 13 bold", command=add_elem)
    add_btn.grid(row=2, column=1, columnspan=2, pady=10, ipadx=145)

    #content_edit.insert('1.0', record[2])


    # Creating a Back Button
    back_btn = Button(new_memo, text="Back", width=5, height=1,bg='#fcd190', border=0, font="Rockwell 13 bold", command=new_memo.destroy)
    back_btn.grid(row=0, column=0, columnspan=1)

    global content
    content = Text(new_memo,border=1, height=32, width=45, font="Calibri 13")
    content.config(highlightthickness=2, highlightbackground='#fcd190')
    content.grid(row=3, column=1)

    content_label = Label(new_memo, text="Memo Content:", border=0, font="Rockwell 13 bold", bg='white')
    content_label.grid(row=3, column=0, ipadx=60)

    save_btn = Button(new_memo, text="Save",bg='#fcd190', border=0, font="Rockwell 13 bold",command=save)
    save_btn.grid(row=6, column=1, columnspan=2, pady=10, ipadx=145)


# Function to update a Memo
def update(id):
    conn = sqlite3.connect('saved_memos.db')
    c = conn.cursor()

    # get the id given as input
    record_id = id
    c.execute("""UPDATE memos SET
        date = :d,
        time = :t,
        content = :c

        WHERE oid = :oid """,
              {
                  'd': datetime.today().strftime('%Y-%m-%d'),
                  't': datetime.today().strftime('%H:%M:%S'),
                  'c': content_edit.get("1.0", "end"),

                  'oid': record_id
              }
              )

    conn.commit()
    conn.close()
    update_main_screen()
    editor.destroy()


# Function to ope an existing memo
def open_memo(id):
    global editor, date, time
    editor = Tk()  # creating the GUI window
    editor.title('Update a record')
    editor.geometry("750x900")
    editor.configure(background='white', border=0)

    conn = sqlite3.connect('saved_memos.db')
    c = conn.cursor()

    record_id = str(id)
    c.execute("SELECT * FROM memos WHERE oid = " + record_id)
    records = c.fetchall()

    # Creating Global Variables for text box names
    global date_edit
    global time_edit
    global content_edit

    content_edit = Text(editor, border=1, height=35, width=45, font="Calibri 13")
    content_edit.config(highlightthickness=2, highlightbackground='#fcd190')
    content_edit.grid(row=3, column=1)

    for record in records:
        date = record[0]
        time = record[1]

    # Creating a Back Button
    back_btn = Button(editor, text="Back", width=5, height=1,bg='#fcd190', border=0, font="Rockwell 13 bold", command=editor.destroy)
    back_btn.grid(row=0, column=0, columnspan=1)

    # Creating the text box Labels
    date_label = Label(editor, text=date, border=0, font="Rockwell 13", bg='white')
    date_label.grid(row=1, column=1)
    time_label = Label(editor,border=0, font="Rockwell 13", bg='white', text="Last edited at:  " + time)
    time_label.grid(row=2, column=1)
    content_label = Label(editor, text="Memo Content:",border=0, font="Rockwell 13", bg='white')
    content_label.grid(row=3, column=0)

    # Create a save button:
    save_btn = Button(editor, text="Save", width=5, height=1,bg='#fcd190', border=0, font="Rockwell 13 bold", command=lambda: update(record_id))
    save_btn.grid(row=6, column=1, columnspan=2, pady=10, padx=10, ipadx=60)

    # Create a delete button:
    delete_btn = Button(editor, text="Delete", width=5, height=1,bg='#fcd190', border=0, font="Rockwell 13 bold", command=lambda: delete(record_id))
    delete_btn.grid(row=6, column=0, columnspan=1, pady=10, padx=10, ipadx=60)

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

    query_label = Label(second_frame, text=print_rec)
    query_label.grid(row=2, column=0, columnspan=2)

    conn.commit()
    conn.close()


# Function to update the notes shown on main screen
def update_main_screen():
    global count
    global buttons
    buttons = []
    for i in range(len(buttons)):
        print("destroying buttons")
        buttons[i].destroy()

    conn = sqlite3.connect('saved_memos.db')
    c = conn.cursor()

    c.execute("SELECT *, oid FROM memos")
    records = c.fetchall()
    count = 2
    # Showing all the existing notes
    for record in records:
        current_rec =  str(record[0]) + " " + str(record[2]).split()[0] + "\n"
        current_id = record[3]
        query_btn = Button(second_frame, text=current_rec, height=2, width=100, border=0, bg='#fcd190', font="Calibri", anchor="w",
                           command=partial(open_memo, current_id))
        query_btn.grid(row=count, column=0, columnspan=3, pady=10, padx=10)
        buttons.append(query_btn)
        count += 1

    conn.commit()
    conn.close()


update_main_screen()
# command=lambda: open(i)


# Create a New memo button
new_btn = Button(root, text="Create new Memo", width=20, height=2, borderwidth=0,bg='#fcd190', font="Rockwell 15 bold",
                 command=new_memo)
new_btn.pack()
# new_btn.grid(row=count+1, column=3, columnspan=1, pady=10, padx=10)

root.mainloop()
