import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from backend.generate import generate_keys

class ImportKeyFrame(tk.Frame):

    def __init__(self, parent, user_folder, username):
        tk.Frame.__init__(self, parent, bg='#ffffff')
        self.pem_file = ''
        self.username = username
        self.use_folder = user_folder
        login_label = tk.Label(
            self, text="Import key", bg='#ffffff', fg="#0011ff", font=("Arial", 30))
        login_label.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=40)

        # Create a dropdown
        dropdown_label = tk.Label(self, text="Algorithm ", font=("Arial", 16), bg='#ffffff')
        dropdown_label.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.dropdown_var = tk.StringVar()
        dropdown_values = ["RSA", "DSA", "ElGammal"]
        dropdown_menu = ttk.OptionMenu(self, self.dropdown_var, dropdown_values[0], *dropdown_values)
        dropdown_menu.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # Key name
        key_name = tk.Label(
            self, text="Key name", bg='#ffffff', fg="#000000", font=("Arial", 16))
        key_name.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.key_entry = tk.Entry(self, font=("Arial", 16))
        self.key_entry.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        button = tk.Button(self, text="Choose File", command=self.choose_file)
        button.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")

        # Create a button
        button = ttk.Button(self, text="Import", command=self.import_key)
        button.grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")
    
    def import_key(self):
        if self.pem_file != '':
            # TODO load files
            print('not implemented')
        
    def choose_file(self):
        self.pem_file = filedialog.askopenfilename(filetypes=[("Pem Files", "*.pem"), ("All Files", "*.*")])
