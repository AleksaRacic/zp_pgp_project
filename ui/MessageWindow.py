import os

import tkinter as tk
from tkinter import filedialog

class MessageWindow:

    def __init__(self, master, message, signed, zipped, enrypted, radix64 ):
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.title("Message")
        self.window.geometry('600x700')
        self.window.configure(bg='#ffffff')
        frame = tk.Frame(self.window, bg='#ffffff')

        signature = tk.Label(
            frame, text="Signature - " + signed, bg='#ffffff', fg="#0011ff", font=("Arial", 10))
        signature.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=2)
        zipp = tk.Label(
            frame, text="Zipped - " + zipped, bg='#ffffff', fg="#0011ff", font=("Arial", 10))
        zipp.grid(row=1, column=2, columnspan=2, sticky="nsew", pady=2)

        enc = tk.Label(
            frame, text="Encrypted - " + enrypted, bg='#ffffff', fg="#0011ff", font=("Arial", 10))
        enc.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=2)
        rad = tk.Label(
            frame, text="Zipped - " + radix64, bg='#ffffff', fg="#0011ff", font=("Arial", 10))
        rad.grid(row=2, column=2, columnspan=2, sticky="nsew", pady=2)

        time_label = tk.Label(
            frame, text="Time sent - " + str(message['timestamp']), bg='#ffffff', fg="#0011ff", font=("Arial", 10))
        time_label.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=10)

        sender_label = tk.Label(
            frame, text="Sender - " + message['sender'], bg='#ffffff', fg="#0011ff", font=("Arial", 10))
        sender_label.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=10)

        subject_label = tk.Label(
            frame, text="Subject - " + message['subject'], bg='#ffffff', fg="#0011ff", font=("Arial", 10))
        subject_label.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=2)

        message_ = tk.Label(
            frame, text=message['message'], bg='#cccccc', fg="#000000", font=("Arial", 8))
        message_.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=2)

        button = tk.Button(frame, text="Save", command=self.save_message)
        button.grid(row=7, column=0, columnspan=2, pady=10, sticky="nsew")
        self.message = message
        frame.pack()

    def save_message(self):
        folder_path = filedialog.askdirectory()
        filename = self.message['subject'] + '_' + str(self.message['timestamp']) + '.txt'
        path = os.path.join(folder_path, filename)
        text = 'Sender: ' + self.message['sender'] +'\n\n' + self.message['message']
        with open(path, "w") as file:
            file.write(text)

    
