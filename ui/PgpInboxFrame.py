import tkinter as tk

class PgpInboxFrame(tk.Frame):

    def __init__(self, parent, user_folder):
        tk.Frame.__init__(self, parent, bg='#0011ff')
        label1 = tk.Label(self, text="Frame 1")
        button1 = tk.Button(self, text="Show Frame 2")
        label1.pack()
        button1.pack()
        