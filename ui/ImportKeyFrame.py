import base64
import datetime
import hashlib
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from backend.generate import generate_keys
from cryptography.hazmat.primitives import serialization
from backend.private_key_ring import PrivateKeyRing
from backend.public_key_ring import PublicKeyRing
from cryptography.hazmat.primitives.asymmetric import rsa, dsa
from Crypto.PublicKey import ElGamal

class ImportKeyFrame(tk.Frame):

    def __init__(self, parent, user_folder, username):
        tk.Frame.__init__(self, parent, bg='#ffffff')
        self.pem_file1 = ''
        self.pem_file2 = ''
        self.username = username
        self.user_folder = user_folder
        login_label = tk.Label(
            self, text="Import key", bg='#ffffff', fg="#0011ff", font=("Arial", 30))
        login_label.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=40)

        # # Create a dropdown
        # dropdown_label = tk.Label(self, text="Algorithm ", font=("Arial", 16), bg='#ffffff')
        # dropdown_label.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        # self.dropdown_var = tk.StringVar()
        # dropdown_values = ["RSA", "DSA", "ElGammal"]
        # dropdown_menu = ttk.OptionMenu(self, self.dropdown_var, dropdown_values[0], *dropdown_values)
        # dropdown_menu.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # Key name
        key_name = tk.Label(
            self, text="Key name", bg='#ffffff', fg="#000000", font=("Arial", 16))
        key_name.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.key_entry = tk.Entry(self, font=("Arial", 16))
        self.key_entry.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        # password
        password = tk.Label(
            self, text="Passphrase", bg='#ffffff', fg="#000000", font=("Arial", 16))
        password.grid(row=3, column=0, sticky="nsew", padx=100, pady=5)
        self.password_entry = tk.Entry(self, font=("Arial", 16))
        self.password_entry.grid(row=3, column=1, padx=10, pady=5, sticky="nsew")

        button = tk.Button(self, text="Choose File - Private Key", command=self.choose_file1)
        button.grid(row=4, column=0, columnspan=2, padx=100, sticky="nsew")

        button = tk.Button(self, text="Choose File - Public Key", command=self.choose_file2)
        button.grid(row=5, column=0, columnspan=2, padx=100, sticky="nsew")

        # Create a button
        button = ttk.Button(self, text="Import", command=self.import_key)
        button.grid(row=6, column=0, columnspan=2, padx=100, sticky="nsew")
    
    def import_key(self):
        if self.pem_file1 == '':
            messagebox.showinfo(message="Error: Select your private key!!!")
        else:
            try:
                # private key
                with open(self.pem_file1, 'rb') as pem_file:
                    private_key = pem_file.read()

                # public key
                public_key = None
                if self.pem_file2 != '':
                    with open(self.pem_file2, 'rb') as pem_file:
                        public_key = pem_file.read()
                
                if public_key == None:
                    try:
                        private_key2 = serialization.load_pem_private_key(
                            private_key,
                            password=self.password_entry.get().encode('utf-8'),  # Optional: provide a password if the PEM is encrypted
                        )
                    except Exception as e:
                        private_key2 = eval((base64.b64decode(private_key)).decode())
                        if private_key2['password'] != self.password_entry.get():
                            messagebox.showinfo(message="Wrong password for private key!")
                        tmp_key_private = private_key2
                        private_key2 = ElGamal.construct((private_key2['p'],private_key2['g'], private_key2['y'], private_key2['x'],))

                    try:
                        public_key = private_key2.public_key()

                        public_key = public_key.public_bytes(
                            encoding=serialization.Encoding.PEM,
                            format=serialization.PublicFormat.SubjectPublicKeyInfo
                        )
                    except Exception as e:
                        tmp_key_public = private_key2.publickey()
                        public_key = base64.b64encode(str({"p": int(tmp_key_public.p), "g": int(tmp_key_public.g), "y": int(tmp_key_public.y), "algorithm": tmp_key_private['algorithm'], "key_size": tmp_key_private['key_size']}).encode())


                key_id = int.from_bytes(hashlib.sha256(public_key).digest()[-8:], byteorder='big')
                
                try:
                    tmp_key_private = serialization.load_pem_private_key(
                        private_key,
                        password=self.password_entry.get().encode('utf-8'),  # Optional: provide a password if the PEM is encrypted
                    )

                    tmp_key_public = serialization.load_pem_public_key(
                        public_key,
                    )
                except Exception as e:
                    private_key = base64.b64encode(str({"p": int(tmp_key_private['p']), "g": int(tmp_key_private['g']), "y": int(tmp_key_private['y']), "x": int(tmp_key_private['x']), "password": tmp_key_private['password'], "algorithm": tmp_key_private['algorithm'], "key_size": tmp_key_private['key_size']}).encode())

                if isinstance(tmp_key_private, rsa.RSAPrivateKey):
                    algorithm = "RSA"
                elif isinstance(tmp_key_private, dsa.DSAPrivateKey):
                    algorithm = "DSA"
                else:
                    algorithm = "ElGamal"

                private_key_info = {
                    'key_id': key_id,
                    'name': self.key_entry.get(),
                    'email': self.username,
                    'algorithm': algorithm,
                    'key_size': tmp_key_private.key_size if algorithm != "ElGamal" else  tmp_key_private['key_size'],
                    'private_key': private_key.decode('utf-8'),
                    'timestamp' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

                public_key_info = {
                    'key_id': key_id,
                    'name': self.key_entry.get(),
                    'email': self.username,
                    'algorithm': algorithm,
                    'key_size': tmp_key_public.key_size if algorithm != "ElGamal" else  tmp_key_private['key_size'],
                    'public_key': public_key.decode('utf-8'),
                    'timestamp' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

                private_key_ring = PrivateKeyRing(self.user_folder.joinpath('keys'))
                public_key_ring = PublicKeyRing(self.user_folder.joinpath('keys'))

                public_key_ring.add_key(public_key_info['key_id'], public_key_info)
                private_key_ring.add_key(public_key_info['key_id'], private_key_info)

                public_key_ring.save()
                private_key_ring.save()
            except ValueError as e:
                messagebox.showinfo(message=e)


        
    def choose_file1(self):
        self.pem_file1 = filedialog.askopenfilename(filetypes=[("Pem Files", "*.pem"), ("All Files", "*.*")])

    def choose_file2(self):
        self.pem_file2 = filedialog.askopenfilename(filetypes=[("Pem Files", "*.pem"), ("All Files", "*.*")])
