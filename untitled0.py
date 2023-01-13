# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 21:19:19 2023

@author: dforc
"""

import tkinter as tk
from tkinter import messagebox

def check_zip(zip_code):
    # function to check if zip code is valid
    if len(zip_code) != 5:
        return False
    if not zip_code.isdigit():
        return False
    return True

def on_submit():
    # function to check zip code and close window if valid
    zip_code = zip_entry.get()
    if check_zip(zip_code):
        root.destroy()
    else:
        messagebox.showerror("Error", "Invalid zip code")

root = tk.Tk()
root.title("Zip Code Entry")

zip_label = tk.Label(root, text="Enter your zip code:")
zip_label.pack()

zip_entry = tk.Entry(root)
zip_entry.pack()

submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack()

while True:
    try:
        root.mainloop()
        break
    except UnicodeDecodeError:
        pass
zip_code = zip_entry.get()