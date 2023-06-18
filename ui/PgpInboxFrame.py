import tkinter as tk
from tkinter import filedialog

class PgpInboxFrame(tk.Frame):

    def __init__(self, parent, user_folder, username):
        tk.Frame.__init__(self, parent, bg='#ffffff')
        self.username = username
        self.user_folder = user_folder
        self.message = None
        self.msg_file = None
        login_label = tk.Label(
            self, text="Inbox", bg='#ffffff', fg="#0011ff", font=("Arial", 30))
        login_label.grid(row=0, column=5, columnspan=2, sticky="nsew", pady=40)


        button = tk.Button(self, text="Choose message from inbox", command=self.choose_file)
        button.grid(row=1, column=5, columnspan=2, pady=10, sticky="nsew")

        if self.message:
            login_label = tk.Label(
                self, text="Verification - ", bg='#ffffff', fg="#0011ff", font=("Arial", 30))
            login_label.grid(row=2, column=5, columnspan=2, sticky="nsew", pady=40)

            login_label = tk.Label(
                self, text="Sender of the message - ", bg='#ffffff', fg="#0011ff", font=("Arial", 30))
            login_label.grid(row=3, column=5, columnspan=2, sticky="nsew", pady=40)

            login_label = tk.Label(
                self, text="Message - ", bg='#ffffff', fg="#0011ff", font=("Arial", 30))
            login_label.grid(row=4, column=3, columnspan=1, sticky="nsew", pady=40)

            button = tk.Button(self, text="Save", command=self.save_message)
            button.grid(row=4, column=3, columnspan=1, pady=10, sticky="nsew")

    
    def choose_file(self):
        self.msg_file = filedialog.askopenfilename(filetypes=[("Message Files", "*.msg"), ("All Files", "*.*")])
        
    def save_message(self):
        pass