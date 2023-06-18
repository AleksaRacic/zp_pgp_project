import tkinter as tk
from .LoginWindow import LoginWindow
from .RegisterWindow import RegisterWindow

class PgpApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Create the main window
        self.title("Login/Register App")

        # Create a frame to hold the buttons
        frame = tk.Frame(self)
        frame.pack(pady=50)
        self.geometry('400x500')

        # Create the Login button
        login_btn = tk.Button(frame, text="Login", width=10, command=self.login)
        login_btn.pack(pady=10)

        # Create the Register button
        register_btn = tk.Button(frame, text="Register", width=10, command=self.register)
        register_btn.pack(pady=10)

    def login(self):
        LoginWindow(self)

    def register(self):
        RegisterWindow(self)
