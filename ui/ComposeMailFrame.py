import datetime
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from backend.generate import generate_keys
from backend.message import SendMessageBuilder
from backend.private_key_ring import PrivateKeyRing
from backend.public_key_ring import PublicKeyRing

class ComposeMailFrame(tk.Frame):
    
    def __init__(self, parent, user_folder, username):
        tk.Frame.__init__(self, parent, bg='#ffffff')
        self.username = username
        self.user_folder = user_folder
        self.is_encrypted = tk.IntVar()
        self.is_base64 = tk.IntVar()
        self.is_signed = tk.IntVar()
        self.is_zipped = tk.IntVar()
        login_label = tk.Label(
            self, text="Send email", bg='#ffffff', fg="#0011ff", font=("Arial", 30))
        login_label.grid(row=0, column=3, columnspan=2, sticky="nsew", pady=40)

        # Checkbox for encryption
        self.encrypt_checkbox = tk.Checkbutton(self, text="Encrypt Message", variable=self.is_encrypted)
        self.encrypt_checkbox.grid(row=1, column=2, columnspan=2, sticky="nsew", pady=4)

        # Checkbox for message signing
        self.sign_checkbox = tk.Checkbutton(self, text="Sign Message", variable=self.is_signed)
        self.sign_checkbox.grid(row=1, column=6, columnspan=2, sticky="nsew", pady=4)

        # Checkbox for compression
        self.compress_checkbox = tk.Checkbutton(self, text="Compress Message", variable=self.is_zipped)
        self.compress_checkbox.grid(row=2, column=2, columnspan=2, sticky="nsew", pady=4)

        # Checkbox for radix-64 format
        self.radix64_checkbox = tk.Checkbutton(self, text="Convert to Radix-64 Format", variable=self.is_base64)
        self.radix64_checkbox.grid(row=2, column=6, columnspan=2, sticky="nsew", pady=4)

        # Input for email
        password = tk.Label(
            self, text="Recipient's email", bg='#ffffff', fg="#000000", font=("Arial", 16))
        password.grid(row=3, column=0, sticky="nsew", padx=5, pady=3)
        self.email = tk.Entry(self, width=50)
        self.email.grid(row=3, column=2, columnspan=2, sticky="nsew", pady=4)

        
        # Input for public key selection
        dropdown_label = tk.Label(self, text="Public Key: ", font=("Arial", 16), bg='#ffffff')
        dropdown_label.grid(row=4, column=0, sticky="nsew", padx=5, pady=3)
        self.dropdown_var = tk.StringVar()
        dropdown_values = self.publicKeys()
        dropdown_menu = ttk.OptionMenu(self, self.dropdown_var, dropdown_values[0], *dropdown_values)
        dropdown_menu.grid(row=4, column=2, padx=5, pady=3, sticky="nsew")

        # Input for private key selection
        dropdown_label = tk.Label(self, text="Private Key: ", font=("Arial", 16), bg='#ffffff')
        dropdown_label.grid(row=4, column=3, sticky="nsew", padx=5, pady=3)
        self.dropdown_var2 = tk.StringVar()
        dropdown_values = self.privateKeys()
        dropdown_menu = ttk.OptionMenu(self, self.dropdown_var2, dropdown_values[0], *dropdown_values)
        dropdown_menu.grid(row=4, column=5, padx=5, pady=3, sticky="nsew")

        # Input for symmetric algorithm selection
        dropdown_label = tk.Label(self, text="Algorithm: ", font=("Arial", 16), bg='#ffffff')
        dropdown_label.grid(row=5, column=0, sticky="nsew", padx=5, pady=3)
        self.dropdown_var3 = tk.StringVar()
        dropdown_values = ["DES3", "AES"]
        dropdown_menu = ttk.OptionMenu(self, self.dropdown_var3, dropdown_values[0], *dropdown_values)
        dropdown_menu.grid(row=5, column=2, padx=5, pady=3, sticky="nsew")

        # Input for subject
        password = tk.Label(
            self, text="Subject", bg='#ffffff', fg="#000000", font=("Arial", 14))
        password.grid(row=6, column=0, sticky="nsew", padx=5, pady=3)
        self.subject = tk.Entry(self, width=65)
        self.subject.grid(row=6, column=2, columnspan=2, sticky="nsew", pady=4)

        # Input for email
        password = tk.Label(
            self, text="Message", bg='#ffffff', fg="#000000", font=("Arial", 14))
        password.grid(row=7, column=0, sticky="nsew", padx=5, pady=3)
        self.message = tk.Entry(self, width=65)
        self.message.grid(row=7, column=2, columnspan=2, sticky="nsew", pady=4)

        # Input for passphrase
        passphrase = tk.Label(
            self, text="Passphrase", bg='#ffffff', fg="#000000", font=("Arial", 14))
        passphrase.grid(row=8, column=0, sticky="nsew", padx=5, pady=3)
        self.passphrase = tk.Entry(self, width=65)
        self.passphrase.grid(row=8, column=2, columnspan=2, sticky="nsew", pady=4)


        # Button to send the message
        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.grid(row=9, column=2, columnspan=2, sticky="nsew", pady=40)

        #---------MOD--------------

        # # Button to send the multiple messages
        # self.send_button = tk.Button(self, text="Send multiple", command=self.send_multiple_message)
        # self.send_button.grid(row=9, column=5, columnspan=2, sticky="nsew", pady=4)

    def publicKeys(self):
        public_key_ring = PublicKeyRing(self.user_folder.joinpath('keys'))
        all_keys = public_key_ring.keys.values()

        return [key['name'] for key in all_keys if key['algorithm'] in ["RSA", "ElGamal"]] # changeme
    
    def privateKeys(self):
        private_key_ring = PrivateKeyRing(self.user_folder.joinpath('keys'))
        all_keys = private_key_ring.keys.values()

        return [key['name'] for key in all_keys if key['algorithm'] in ["RSA", "DSA"]]

    def send_message(self):
        
        print(self.is_base64.get())

        private_key_name = self.dropdown_var2.get()
        public_key_name = self.dropdown_var.get()

        public_key_ring = PublicKeyRing(self.user_folder.joinpath('keys'))
        private_key_ring = PrivateKeyRing(self.user_folder.joinpath('keys'))

        private_key = [key for key in private_key_ring.keys.values() if key['name'] == private_key_name][0]
        public_key = [key for key in public_key_ring.keys.values() if key['name'] == public_key_name][0]

        print(private_key, public_key)

        if (self.is_encrypted.get() and self.is_signed.get()) and ((private_key['algorithm'] == "RSA" and public_key['algorithm'] != "RSA") or
            (private_key['algorithm'] == "DSA" and public_key['algorithm'] != "ElGamal")):
            messagebox.showinfo(message=f"when the private key type is {private_key['algorithm']}, then the public key type must not be {public_key['algorithm']}")
            return


        msgBuilder = SendMessageBuilder(self.message.get(), self.subject.get(), self.username)

        if self.is_signed.get():
            msgBuilder.sign(private_key=private_key['private_key'], password=self.passphrase.get(), private_key_id=private_key['key_id'], private_key_algorithm=private_key['algorithm'])
        
        if self.is_zipped.get():
            msgBuilder.zip()

        if self.is_encrypted.get():
            msgBuilder.encrypt(self.dropdown_var3.get(), public_key['public_key'], public_key['key_id'], public_key['algorithm'])

        if self.is_base64.get():
            msgBuilder.to_base64()

        msg = msgBuilder.build()
        
        # PATH
        current_directory = os.getcwd()

        path = os.path.join(current_directory, 'pgp_data', self.email.get(), 'inbox', self.username + '_' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.msg')

        try:
            with open(path, 'wb') as f:
                f.write(msg)
        except Exception as e:
            messagebox.showinfo(message=f"No user with email - {self.email.get()}")
            return
        
        messagebox.showinfo(message="Email successfully sent")
        print(msg)



    # -------MOD----------

    # def send_message_mod(self, email, public_key_name):

    #     private_key_name = self.dropdown_var2.get()

    #     public_key_ring = PublicKeyRing(self.user_folder.joinpath('keys'))
    #     private_key_ring = PrivateKeyRing(self.user_folder.joinpath('keys'))

    #     private_key = [key for key in private_key_ring.keys.values() if key['name'] == private_key_name][0]
    #     public_key = [key for key in public_key_ring.keys.values() if key['name'] == public_key_name][0]

    #     print(private_key, public_key)

    #     if (self.is_encrypted.get() and self.is_signed.get()) and ((private_key['algorithm'] == "RSA" and public_key['algorithm'] != "RSA") or
    #         (private_key['algorithm'] == "DSA" and public_key['algorithm'] != "ElGamal")):
    #         messagebox.showinfo(message=f"when the private key type is {private_key['algorithm']}, then the public key type must not be {public_key['algorithm']}")
    #         return


    #     msgBuilder = SendMessageBuilder(self.message.get(), self.subject.get(), self.username)

    #     if self.is_signed.get():
    #         msgBuilder.sign(private_key=private_key['private_key'], password=self.passphrase.get(), private_key_id=private_key['key_id'], private_key_algorithm=private_key['algorithm'])
        
    #     if self.is_zipped.get():
    #         msgBuilder.zip()

    #     if self.is_encrypted.get():
    #         msgBuilder.encrypt(self.dropdown_var3.get(), public_key['public_key'], public_key['key_id'], public_key['algorithm'])

    #     if self.is_base64.get():
    #         msgBuilder.to_base64()

    #     msg = msgBuilder.build()
        
    #     # PATH
    #     current_directory = os.getcwd()

    #     path = os.path.join(current_directory, 'pgp_data', email, 'inbox', self.username + '_' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.msg')

    #     try:
    #         with open(path, 'wb') as f:
    #             f.write(msg)
    #     except Exception as e:
    #         messagebox.showinfo(message=f"No user with email - {email}")
    #         return
        
    #     messagebox.showinfo(message="Email successfully sent")
    #     print(msg)

    
    # def send_multiple_message(self):

    #     #emails should be splitted with ; - like masha;ziza

    #     emails = self.email.get().split(';')

    #     for email in emails:
    #         selected_option = simpledialog.askstring("Select", f"For mail {email} ,enter a name of possible public keys - {self.publicKeys()}:")
    #         self.send_message_mod(email, selected_option)





            



