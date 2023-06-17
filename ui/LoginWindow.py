import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import json

from PgpWindow import PgpWindow

class LoginWindow:

    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.title("Login form")
        self.window.geometry('400x500')
        self.window.configure(bg='#ffffff')
        frame = tk.Frame(self.window, bg='#ffffff')

        login_label = tk.Label(
            frame, text="Login", bg='#ffffff', fg="#0011ff", font=("Arial", 30))
        username_label = tk.Label(
            frame, text="Username", bg='#ffffff', fg="#000000", font=("Arial", 16))
        self.username_entry = tk.Entry(frame, font=("Arial", 16))
        self.password_entry = tk.Entry(frame, show="*", font=("Arial", 16))
        password_label = tk.Label(
            frame, text="Password", bg='#ffffff', fg="#000000", font=("Arial", 16))
        login_button = tk.Button(
            frame, text="Login", bg="#0011ff", fg="#FFFFFF", font=("Arial", 16), command=self.login)

        
        password_label.grid(row=2, column=0)
        login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
        username_label.grid(row=1, column=0)
        login_button.grid(row=3, column=0, columnspan=2, pady=30)

        self.username_entry.grid(row=1, column=1, pady=20)
        self.password_entry.grid(row=2, column=1, pady=20)

        frame.pack()

    def login(self):
        pgp_data = Path("./pgp_data")
        folder_path = pgp_data.joinpath(self.username_entry.get())
        file_path = folder_path.joinpath('user.json')

        with open(file_path, "r") as file:
            data = json.load(file)

        if self.username_entry.get()==data['username'] and self.password_entry.get()==data['password']:
            PgpWindow(self.master, folder_path)
            self.window.destroy()
        else:
            messagebox.showerror(title="Error", message="Invalid login.")

    
