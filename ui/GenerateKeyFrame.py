import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from backend.generate import generate_keys
from backend.private_key_ring import PrivateKeyRing
from backend.public_key_ring import PublicKeyRing

class GenerateKeyFrame(tk.Frame):

    def __init__(self, parent, user_folder, username):
        tk.Frame.__init__(self, parent, bg='#ffffff')
        self.username = username
        self.user_folder = user_folder
        login_label = tk.Label(
            self, text="Genereate key", bg='#ffffff', fg="#0011ff", font=("Arial", 30))
        login_label.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=40)

        # Create a dropdown
        dropdown_label = tk.Label(self, text="Algorithm ", font=("Arial", 16), bg='#ffffff')
        dropdown_label.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.dropdown_var = tk.StringVar()
        dropdown_values = ["RSA", "DSA", "ElGamal"]
        dropdown_menu = ttk.OptionMenu(self, self.dropdown_var, dropdown_values[0], *dropdown_values)
        dropdown_menu.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # Create a text input
        password_label = tk.Label(
            self, text="Password", bg='#ffffff', fg="#000000", font=("Arial", 16))
        password_label.grid(row=2, column=0, sticky="nsew")
        self.password_entry = tk.Entry(self, show="*", font=("Arial", 16))
        self.password_entry.grid(row=2, column=1, pady=20, sticky="nsew")

        # Create a dropdown
        dropdown_label = tk.Label(self, text="Key Size ", font=("Arial", 16), bg='#ffffff')
        dropdown_label.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.key_size_var = tk.IntVar()
        dropdown_values = [1024, 2048]
        dropdown_menu = ttk.OptionMenu(self, self.key_size_var, dropdown_values[0], *dropdown_values)
        dropdown_menu.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

        # Key name
        key_name = tk.Label(
            self, text="Key name", bg='#ffffff', fg="#000000", font=("Arial", 16))
        key_name.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
        self.key_entry = tk.Entry(self, font=("Arial", 16))
        self.key_entry.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")

        # Create a button
        button = ttk.Button(self, text="Submit", command=self.generate_keys)
        button.grid(row=5, column=0, columnspan=2, pady=10, sticky="nsew")
    
    def generate_keys(self):
        key_name = self.key_entry.get()
        algorithm = self.dropdown_var.get()
        key_size = self.key_size_var.get()
        password = self.password_entry.get()
        private_key_info,public_key_info = generate_keys(key_name, self.username, algorithm, key_size, password)

        private_key_ring = PrivateKeyRing(self.user_folder.joinpath('keys'))
        public_key_ring = PublicKeyRing(self.user_folder.joinpath('keys'))

        public_key_ring.add_key(public_key_info['key_id'], public_key_info)
        private_key_ring.add_key(public_key_info['key_id'], private_key_info)

        public_key_ring.save()
        private_key_ring.save()
        messagebox.showinfo(message="Keys successfully created")


        
