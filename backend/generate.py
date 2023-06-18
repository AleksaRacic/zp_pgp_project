import base64
import datetime
import hashlib
import os
from .private_key_ring import PrivateKeyRing
from .public_key_ring import PublicKeyRing
from cryptography.hazmat.primitives.asymmetric import rsa, dsa
from Crypto.PublicKey import ElGamal
from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives import serialization
from Crypto.IO import PEM

from cryptography.hazmat.backends import default_backend

from asn1crypto import keys, pem


def generate_and_serialize_keys(key_size, algorithm, passphrase):

    if algorithm == "RSA":
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        public_key = private_key.public_key()
    elif algorithm == "DSA":
        private_key = dsa.generate_private_key(
            key_size=key_size
        )
        public_key = private_key.public_key()
    elif algorithm == "ElGamal":
        private_key = ElGamal.generate(key_size, get_random_bytes)
        public_key = private_key.publickey()
    else:
        raise TypeError
    

    if algorithm != "ElGamal":
        encryption_algorithm = serialization.BestAvailableEncryption(password=passphrase.encode('utf-8'))
        pem_private = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption_algorithm
        )

        pem_public = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    else:
        
        pem_public = base64.b64encode(str({"p": int(public_key.p), "g": int(public_key.g), "y": int(public_key.y), "algorithm": algorithm, "key_size": key_size}).encode())
        pem_private = base64.b64encode(str({"p": int(private_key.p), "g": int(private_key.g), "y": int(private_key.y), "x": int(private_key.x), "password": passphrase, "algorithm": algorithm, "key_size": key_size}).encode())



    return pem_private, pem_public, passphrase

def export_keys(key):
    
    if key['private_key']:
        path = os.path.join('keys', 'private_keys', f'{key["email"]}.pem')
        os.makedirs(path, exist_ok=True)
        file_path = os.path.join(path, f'{key["email"]}.pem')
        with open(file_path, 'wb') as f:
            f.write(key['private_key'].encode('utf-8'))
    elif key['public_key']:
        path = os.path.join('keys', 'public_keys', f'{key["email"]}.pem')
        os.makedirs(path, exist_ok=True)
        file_path = os.path.join(path, f'{key["email"]}.pem')
        with open(file_path, 'wb') as f:
            f.write(key['public_key'].encode('utf-8'))

def generate_keys(name, email, algorithm, key_size, passphrase):

    try:
        private_key, public_key, passphrase = generate_and_serialize_keys(key_size=key_size, algorithm=algorithm, passphrase=passphrase)
    except Exception as e:
        print(e)
    
    key_id = int.from_bytes(hashlib.sha256(public_key).digest()[-8:], byteorder='big')

    private_key_info = {
        'key_id': key_id,
        'name': name,
        'email': email,
        'algorithm': algorithm,
        'key_size': key_size,
        'private_key': private_key.decode('utf-8'),
        'timestamp' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    public_key_info = {
        'key_id': key_id,
        'name': name,
        'email': email,
        'algorithm': algorithm,
        'key_size': key_size,
        'public_key': public_key.decode('utf-8'),
        'timestamp' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    return private_key_info,public_key_info
     

# za testiranje
def main():

    private_key_ring = PrivateKeyRing()
    public_key_ring = PublicKeyRing()

    # promenljive koje trebaju sa fronta da se povuku
    name = "Tasha"
    email = "tasha@gmail.com"
    # terba da bude drop-down lista sa RSA, DSA ili ElGamal
    algorithm = "ElGamal"
    # terba da bude drop-down lista sa 1024 ili 2048
    key_size = 1024
    passphrase = "tasha123"
    private_key_info,public_key_info = generate_keys(name, email, algorithm, key_size, passphrase)

    public_key_ring.add_key(public_key_info['key_id'], public_key_info)
    private_key_ring.add_key(public_key_info['key_id'], private_key_info)

    export_keys(private_key_info)







if __name__ == '__main__':
    main()
