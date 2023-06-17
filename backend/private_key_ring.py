import json

class PrivateKeyRing:
    def __init__(self, keys_folder):
        self.keys_folder = keys_folder
        self.filepath = keys_folder.joinpath('private_key_ring.json')
        if self.filepath.is_file():
            with self.filepath.open(mode='r') as file:
                self.keys = json.load(file)
            print(self.keys)
        else:
            self.keys = dict()

    def add_key(self, key_id, info):
        self.keys[key_id] = info

    def get_key(self, key_id):
        return self.keys.get(key_id)

    def remove_key(self, key_id):
        if key_id in self.keys:
            del self.keys[key_id]
    
    def get_items(self):
        return self.keys.values()
    
    def save(self):
        with open(self.filepath, "w") as file:
            json.dump(self.keys, file)
