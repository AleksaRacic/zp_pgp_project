import tkinter as tk
from tkinter import ttk
from backend.generate import generate_keys
from backend.private_key_ring import PrivateKeyRing
from backend.public_key_ring import PublicKeyRing

class ComposeMailFrame(tk.Frame):
    
    def __init__(self, parent, user_folder, username):
        tk.Frame.__init__(self, parent, bg='#ffffff')
        self.username = username
        self.user_folder = user_folder
        login_label = tk.Label(
            self, text="Send email", bg='#ffffff', fg="#0011ff", font=("Arial", 30))
        login_label.grid(row=0, column=3, columnspan=2, sticky="nsew", pady=40)

        # Checkbox for encryption
        self.encrypt_checkbox = tk.Checkbutton(self, text="Encrypt Message")
        self.encrypt_checkbox.grid(row=1, column=2, columnspan=2, sticky="nsew", pady=40)

        # Checkbox for message signing
        self.sign_checkbox = tk.Checkbutton(self, text="Sign Message")
        self.sign_checkbox.grid(row=1, column=6, columnspan=2, sticky="nsew", pady=40)

        # Checkbox for compression
        self.compress_checkbox = tk.Checkbutton(self, text="Compress Message")
        self.compress_checkbox.grid(row=2, column=2, columnspan=2, sticky="nsew", pady=40)

        # Checkbox for radix-64 format
        self.radix64_checkbox = tk.Checkbutton(self, text="Convert to Radix-64 Format")
        self.radix64_checkbox.grid(row=2, column=6, columnspan=2, sticky="nsew", pady=40)

        # Input for email
        password = tk.Label(
            self, text="Recipient's email", bg='#ffffff', fg="#000000", font=("Arial", 16))
        password.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.email = tk.Entry(self, width=50)
        self.email.grid(row=3, column=2, columnspan=2, sticky="nsew", pady=40)

        # Input for public key selection
        dropdown_label = tk.Label(self, text="Public Key: ", font=("Arial", 16), bg='#ffffff')
        dropdown_label.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
        self.dropdown_var = tk.StringVar()
        dropdown_values = self.publicKeys()
        dropdown_menu = ttk.OptionMenu(self, self.dropdown_var, dropdown_values[0], *dropdown_values)
        dropdown_menu.grid(row=4, column=4, padx=5, pady=5, sticky="nsew")

        # Input for private key selection
        dropdown_label = tk.Label(self, text="Private Key: ", font=("Arial", 16), bg='#ffffff')
        dropdown_label.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)
        self.dropdown_var = tk.StringVar()
        dropdown_values = self.privateKeys()
        dropdown_menu = ttk.OptionMenu(self, self.dropdown_var, dropdown_values[0], *dropdown_values)
        dropdown_menu.grid(row=5, column=4, padx=5, pady=5, sticky="nsew")

        # Input for symmetric algorithm selection
        dropdown_label = tk.Label(self, text="Algorithm: ", font=("Arial", 16), bg='#ffffff')
        dropdown_label.grid(row=6, column=0, sticky="nsew", padx=5, pady=5)
        self.dropdown_var = tk.StringVar()
        dropdown_values = ["TripleDES", "AES128"]
        dropdown_menu = ttk.OptionMenu(self, self.dropdown_var, dropdown_values[0], *dropdown_values)
        dropdown_menu.grid(row=6, column=4, padx=5, pady=5, sticky="nsew")

        # Input for email
        password = tk.Label(
            self, text="Message", bg='#ffffff', fg="#000000", font=("Arial", 14))
        password.grid(row=7, column=0, sticky="nsew", padx=5, pady=5)
        self.email = tk.Entry(self, width=65)
        self.email.grid(row=7, column=2, columnspan=2, sticky="nsew", pady=40)


        # Button to send the message
        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.grid(row=8, column=2, columnspan=2, sticky="nsew", pady=40)

    def send_message(self):
        #send message
        pass

    def publicKeys(self):
        public_key_ring = PublicKeyRing(self.user_folder.joinpath('keys'))
        all_keys = public_key_ring.keys.values()

        return [key['name'] for key in all_keys if key['algorithm'] in ["DSA", "ElGamal"]] # changeme
    
    def privateKeys(self):
        private_key_ring = PrivateKeyRing(self.user_folder.joinpath('keys'))
        all_keys = private_key_ring.keys.values()

        return [key['name'] for key in all_keys if key['algorithm'] in ["RSA", "DSA"]]
