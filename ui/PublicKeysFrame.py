import tkinter as tk
import os
from tkinter import ttk
from tkinter import filedialog
from backend.private_key_ring import PrivateKeyRing

from backend.public_key_ring import PublicKeyRing

class PublicKeysFrame(tk.Frame):

    def __init__(self, parent, user_folder, username):
        tk.Frame.__init__(self, parent, bg='#ffffff')
        
        self.username = username
        self.user_folder = user_folder
        self.public_key_ring = PublicKeyRing(self.user_folder.joinpath('keys'))
        self.private_key_ring = PrivateKeyRing(self.user_folder.joinpath('keys'))

        login_label = tk.Label(
            self, text="Public Keys", bg='#ffffff', fg="#0011ff", font=("Arial", 30))
        login_label.pack()

        # Create the Treeview widget
        self.tree = ttk.Treeview(self, columns=("key_id", "name", "email", "algorithm", "key_size"))

        # Define column headings
        self.tree.heading("key_id", text="key_id")
        self.tree.heading("name", text="name")
        self.tree.heading("email", text="email")
        self.tree.heading("algorithm", text="algorithm")
        self.tree.heading("key_size", text="key_size")

        # Configure column widths
        self.tree.column("key_id", width=200)
        self.tree.column("name", width=100)
        self.tree.column("email", width=100)
        self.tree.column("algorithm", width=100)
        self.tree.column("key_size", width=100)

        self.populate_tree()

        # Add a button to each row
        for item in self.tree.get_children():
            self.tree.insert(item, "end", text="Delete", values=("", "", ""), tags=("delete_button",))
            self.tree.insert(item, "end", text="Export", values=("", "", ""), tags=("export_button",))

        self.tree.tag_bind("delete_button", "<Button-1>", self.delete_row)
        self.tree.tag_bind("export_button", "<Button-1>", self.export_row)

        # Pack the self.treeview widget
        self.tree.pack()

    # Callback function to delete a row and get column values
    def delete_row(self, event):
        selected_item = self.tree.selection()
        values = self.tree.item(selected_item, "values")
        key_id = values[0]
        self.public_key_ring.remove_key(key_id)
        self.public_key_ring.save()
        self.private_key_ring.remove_key(key_id)
        self.private_key_ring.save()
        # print('Deleted key ', key_id)
        self.tree.delete(selected_item)
    
    def export_row(self, event):
        selected_item = self.tree.selection()
        values = self.tree.item(selected_item, "values")
        key_id = values[0]
        folder_path = filedialog.askdirectory()
        path = os.path.join(folder_path, values[1] + '_' + values[0])
        self.public_key_ring.export(key_id, path)
    
    def populate_tree(self):
        for item in self.public_key_ring.get_items():
            self.tree.insert("", "end", values=(item['key_id'], item['name'], item['email'], item['algorithm'], item['key_size']))





        