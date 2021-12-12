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



# Create a New memo button
new_btn= Button(root, text="Create new Memo")
new_btn.grid(row=3, column=2, columnspan=1, pady=10, padx=10)

root.mainloop()
