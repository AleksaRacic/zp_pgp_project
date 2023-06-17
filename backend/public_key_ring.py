class PublicKeyRing:
    def __init__(self):
        self.keys = {}

    def add_key(self, key_id, info):
        self.keys[key_id] = info

    def get_key(self, key_id):
        return self.keys.get(key_id)

    def remove_key(self, key_id):
        if key_id in self.keys:
            del self.keys[key_id]
