import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class ImportKeyFrame(tk.Frame):

    def __init__(self, parent, user_folder, username):
        tk.Frame.__init__(self, parent, bg='#ffffff')
        self.pem_file = ''
        self.username = username
        self.use_folder = user_folder
        login_label = tk.Label(
            self, text="Private Keys", bg='#ffffff', fg="#0011ff", font=("Arial", 30))
        login_label.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=40)

        