import tkinter as tk

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
        signature.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=10)
        zipp = tk.Label(
            frame, text="Zipped - " + zipped, bg='#ffffff', fg="#0011ff", font=("Arial", 10))
        zipp.grid(row=1, column=2, columnspan=2, sticky="nsew", pady=10)

        enc = tk.Label(
            frame, text="Encrypted - " + enrypted, bg='#ffffff', fg="#0011ff", font=("Arial", 10))
        enc.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)
        rad = tk.Label(
            frame, text="Zipped - " + radix64, bg='#ffffff', fg="#0011ff", font=("Arial", 10))
        rad.grid(row=2, column=2, columnspan=2, sticky="nsew", pady=10)

        sender_label = tk.Label(
            frame, text="Sender - " + message['sender'], bg='#ffffff', fg="#0011ff", font=("Arial", 10))
        sender_label.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=10)

        subject_label = tk.Label(
            frame, text="Subject - " + message['subject'], bg='#ffffff', fg="#0011ff", font=("Arial", 10))
        subject_label.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=10)

        message = tk.Label(
            frame, text="Subject - " + message['message'], bg='#ffffff', fg="#0011ff", font=("Arial", 10))
        message.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=10)

        button = tk.Button(frame, text="Save", command=self.save_message)
        button.grid(row=6, column=0, columnspan=1, pady=10, sticky="nsew")

        frame.pack()

    def save_message(self):
        pass

    
