import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from .PgpInboxFrame import PgpInboxFrame
from .GenerateKeyFrame import GenerateKeyFrame
from .ImportKeyFrame import ImportKeyFrame
from .PrivateKeysFrame import PrivateKeysFrame


class PgpWindow:

    def __init__(self, master, user_folder, username):
        self.username = username
        self.user_folder = user_folder
        self.window = tk.Toplevel(master)
        self.window.title("PGP mail")
        self.window.geometry('1000x1000')
        self.window.configure(bg='#ffffff')

        mainmenu = tk.Menu(self.window)
        self.window.config(menu=mainmenu)

        mailmenu = tk.Menu(mainmenu)
        mainmenu.add_cascade(label="Mail", menu=mailmenu)
        mailmenu.add_command(label="Inbox", command=self.setPgpInboxFrame)
        mailmenu.add_command(label="Compose", command=lambda:print("Compose"))

        keymenu = tk.Menu(mainmenu)
        mainmenu.add_cascade(label="Keys", menu=keymenu)
        keymenu.add_command(label="Show Private Keys", command=self.setPrivateKeysFrame)
        keymenu.add_command(label="Import Key", command=self.setImportKeyFrame)
        keymenu.add_command(label="Generate Key", command=self.setGenerateKeyFrame)
        
        self.curr_frame = PgpInboxFrame(self.window, user_folder)
        self.curr_frame.pack(fill=tk.BOTH, expand=True)

    def set_new_frame(self, newFrame):
        self.curr_frame.pack_forget()
        self.curr_frame.destroy()
        self.curr_frame = newFrame
        newFrame.pack(fill=tk.BOTH, expand=True)

    def setPgpInboxFrame(self):
        frame = PgpInboxFrame(self.window, self.user_folder)
        self.set_new_frame(frame)

    def setGenerateKeyFrame(self):
        frame = GenerateKeyFrame(self.window, self.user_folder, self.username)
        self.set_new_frame(frame)
    
    def setImportKeyFrame(self):
        frame = ImportKeyFrame(self.window, self.user_folder, self.username)
        self.set_new_frame(frame)
    
    def setImportKeyFrame(self):
        frame = ImportKeyFrame(self.window, self.user_folder, self.username)
        self.set_new_frame(frame)
    
    def setPrivateKeysFrame(self):
        frame = PrivateKeysFrame(self.window, self.user_folder, self.username)
        self.set_new_frame(frame)
