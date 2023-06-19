import tkinter as tk
from .LoginWindow import LoginWindow
from .RegisterWindow import RegisterWindow

class PgpApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("PGP Launcher")

        frame = tk.Frame(self)
        frame.pack(pady=50)
        self.geometry('400x500')

        pgp_label = tk.Label(
            frame, text="PGP mailbox", fg="#0011ff", font=("Arial", 30))

        login_button = tk.Button(
            frame, text="Login", bg="#0011ff", fg="#FFFFFF", font=("Arial", 16), command=self.login)

        register_btn = tk.Button(
            frame, text="Register", bg="#0011ff", fg="#FFFFFF", font=("Arial", 16), command=self.register)
        
        pgp_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
        login_button.grid(row=1, column=0, columnspan=2, sticky="news", pady=40)
        register_btn.grid(row=2, column=0, columnspan=2, sticky="news", pady=40)
        

        

    def login(self):
        LoginWindow(self)

    def register(self):
        RegisterWindow(self)
