# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 22:42:04 2023

@author: dforc
"""

import tkinter as tk

def get_zip():
    zip = entry.get()
    print("Zip code:", zip)

root = tk.Tk()
root.title("Zip Code")

label = tk.Label(root, text="Enter your zip code:")
label.pack()

entry = tk.Entry(root)
entry.pack()

submit = tk.Button(root, text="Submit", command=get_zip)
submit.pack()

root.mainloop()