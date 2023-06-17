import hashlib
import os
from private_key_ring import PrivateKeyRing
from public_key_ring import PublicKeyRing
from cryptography.hazmat.primitives.asymmetric import rsa, dsa
# from Crypto.PublicKey import ElGamalKey
from Crypto.Math.Numbers import Integer
from Crypto.Math.Primality import generate_probable_prime
from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives import serialization


# def generate_elgamal_keys(bits, randfunc):

#     obj=ElGamalKey()

#     # Generate a safe prime p
#     # See Algorithm 4.86 in Handbook of Applied Cryptography
#     obj.p = generate_probable_prime(exact_bits=bits, randfunc=randfunc)
#     q = (obj.p - 1) >> 1

#     # Generate generator g
#     while 1:
#         # Choose a square residue; it will generate a cyclic group of order q.
#         obj.g = pow(Integer.random_range(min_inclusive=2,
#                                      max_exclusive=obj.p,
#                                      randfunc=randfunc), 2, obj.p)

#         # We must avoid g=2 because of Bleichenbacher's attack described
#         # in "Generating ElGamal signatures without knowning the secret key",
#         # 1996
#         if obj.g in (1, 2):
#             continue

#         # Discard g if it divides p-1 because of the attack described
#         # in Note 11.67 (iii) in HAC
#         if (obj.p - 1) % obj.g == 0:
#             continue

#         # g^{-1} must not divide p-1 because of Khadir's attack
#         # described in "Conditions of the generator for forging ElGamal
#         # signature", 2011
#         ginv = obj.g.inverse(obj.p)
#         if (obj.p - 1) % ginv == 0:
#             continue

#         # Found
#         break

#     # Generate private key x
#     obj.x = Integer.random_range(min_inclusive=2,
#                                  max_exclusive=obj.p-1,
#                                  randfunc=randfunc)
#     # Generate public key y
#     obj.y = pow(obj.g, obj.x, obj.p)
#     return obj

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
        # private_key = generate_elgamal_keys(key_size, get_random_bytes)
        # public_key = private_key.publickey()
        pass
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

def export_keys(key):
    
    if key['private_key']:
        path = os.path.join('keys', 'private_keys', f'{key["email"]}.pem')
        os.makedirs(path, exist_ok=True)
        file_path = os.path.join(path, f'{key["email"]}.pem')
        with open(file_path, 'wb') as f:
            f.write(key['private_key'])
    elif key['public_key']:
        path = os.path.join('keys', 'public_keys', f'{key["email"]}.pem')
        os.makedirs(path, exist_ok=True)
        file_path = os.path.join(path, f'{key["email"]}.pem')
        with open(file_path, 'wb') as f:
            f.write(key['public_key'])

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
    algorithm = "DSA"
    # terba da bude drop-down lista sa 1024 ili 2048
    key_size = 1024

    private_key_info,public_key_info = generate_keys(name, email, algorithm, key_size)

    public_key_ring.add_key(public_key_info['key_id'], public_key_info)
    private_key_ring.add_key(public_key_info['key_id'], private_key_info)

    export_keys(private_key_info)







if __name__ == '__main__':
    main()
