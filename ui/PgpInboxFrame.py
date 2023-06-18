import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog

import time

from backend.message import *
from backend.generate import *
from .MessageWindow import MessageWindow 

class PgpInboxFrame(tk.Frame):

    def __init__(self, parent, user_folder, username):
        tk.Frame.__init__(self, parent, bg='#ffffff')

        self.parent = parent
        self.username = username
        self.user_folder = user_folder

        self.signed = False
        self.message = None
        self.msg_file = None


        login_label = tk.Label(
            self, text="Inbox", bg='#ffffff', fg="#0011ff", font=("Arial", 30))
        login_label.grid(row=0, column=5, columnspan=2, sticky="nsew", pady=40)


        button = tk.Button(self, text="Choose message from inbox", command=self.choose_file)
        button.grid(row=1, column=5, columnspan=2, pady=10, sticky="nsew")
    
    def choose_file(self):
        msg_file = filedialog.askopenfilename(filetypes=[("Message Files", "*.msg"), ("All Files", "*.*")])
        with open(msg_file, "rb") as file:
            msg = file.read()
        print(msg)

        self.signature = 'No signature'
        self.encripted = 'Not Encrypted'
        self.zipped = 'Not zipped'
        self.format = 'Not Radix-64'
        msgReceiver1 = ReceiveMsgBuilder(msg)

        if msgReceiver1.is_base64():
            self.format = 'Radix-64'
            msgReceiver1.decode_base64()
        if msgReceiver1.is_encripted():
            self.private_key_id = msgReceiver1.get_encription_key_id()

            private_key_ring = PrivateKeyRing(self.user_folder.joinpath('keys'))
            private_key_info = private_key_ring.get_key(self.private_key_id)

            if private_key_info == None:
                messagebox.showerror(title="Error", message="No key id =" + str(private_key_info['key_id']) + " in private key ring")
            
            self.password = simpledialog.askstring("Password Entry for key " + private_key_info['name'], "Password for " + private_key_info['name'], show='*')

            msgReceiver1.decrypt(private_key_info['private_key'], self.password)
            print(msgReceiver1.build())
            self.encripted = 'Encrypted'
        if msgReceiver1.check_zip():
            self.zipped = 'Zipped'
            msgReceiver1.unzip()
        if msgReceiver1.is_signed():
            public_key_id = msgReceiver1.get_signature_key_id()

            public_key_ring = PublicKeyRing(self.user_folder.joinpath('keys'))

            public_key_info = public_key_ring.get_key(public_key_id)

            if public_key_info == None:
                messagebox.showerror(title="Error", message="No key id =" + str(public_key_id) + " in public key ring")
            
            if msgReceiver1.verify_signature(public_key_info['public_key']):
                self.signature = 'Good signature'
            else:
                self.signature = 'Bad signature'
            msgReceiver1.remove_signature()
        self.message = msgReceiver1.build()

        MessageWindow(self.parent, self.message, self.signature, self.zipped,self.encripted, self.format)
    
    def save_message(self):
        pass