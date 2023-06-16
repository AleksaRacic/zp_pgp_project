import hashlib
from private_key_ring import PrivateKeyRing
from public_key_ring import PublicKeyRing
from cryptography.hazmat.primitives.asymmetric import rsa, dsa
from Crypto.PublicKey import ElGamal
from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives import serialization

def generate_and_serialize_keys(key_size, algorithm):

    if algorithm == "RSA":
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size
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
    

    # sa fronta lozinka koju je uneo sam korisnik
    passphrase = "tasha123"
    encryption_algorithm = serialization.BestAvailableEncryption(password=passphrase.encode())
    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption_algorithm
    )

    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return pem_private, pem_public, passphrase

def generate_keys(name, email, algorithm, key_size):

    try:
        private_key, public_key, passphrase = generate_and_serialize_keys(key_size=key_size, algorithm=algorithm)
    except Exception as e:
        print(e)
    
    key_id = int.from_bytes(hashlib.sha256(public_key).digest()[-8:], byteorder='big')

    private_key_info = {
        'key_id': key_id,
        'name': name,
        'email': email,
        'algorithm': algorithm,
        'key_size': key_size,
        'private_key': private_key
    }

    public_key_info = {
        'key_id': key_id,
        'name': name,
        'email': email,
        'algorithm': algorithm,
        'key_size': key_size,
        'public_key': public_key
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

    private_key_info,public_key_info = generate_keys(name, email, algorithm, key_size)

    public_key_ring.add_key(public_key_info['key_id'], public_key_info)
    private_key_ring.add_key(public_key_info['key_id'], private_key_info)







if __name__ == '__main__':
    main()
