import json

class PrivateKeyRing:
    def __init__(self, keys_folder):
        self.keys_folder = keys_folder
        self.keys = {}

    def add_key(self, key_id, info):
        self.keys[key_id] = info

    def get_key(self, key_id):
        return self.keys.get(key_id)

    def remove_key(self, key_id):
        if key_id in self.keys:
            del self.keys[key_id]
    
    def save(self):
        with open(self.keys_folder.joinpath('private_key_ring.json'), "w") as file:
            json.dump(self.keys, file)
