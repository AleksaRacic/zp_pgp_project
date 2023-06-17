import tkinter as tk
from tkinter import ttk
from backend.generate import generate_keys

class GenerateKeyFrame(tk.Frame):

    def __init__(self, parent, user_folder):
        tk.Frame.__init__(self, parent, bg='#ffffff')

        login_label = tk.Label(
            self, text="Genereate key", bg='#ffffff', fg="#0011ff", font=("Arial", 30))
        login_label.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=40)

        # Create a dropdown
        dropdown_label = tk.Label(self, text="Algorithm ", font=("Arial", 16), bg='#ffffff')
        dropdown_label.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.dropdown_var = tk.StringVar()
        dropdown_values = ["RSA", "DSA", "ElGammal"]
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

        

        # Create a button
        button = ttk.Button(self, text="Submit", command=self.generate_keys)
        button.grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")
    
    def generate_keys(self):
        user = "test"
        algorithm = self.dropdown_var.get()
        key_size = self.key_size_var.get()
        password = self.password_entry.get()
        print(generate_keys(user, user, algorithm, key_size, password))
        
