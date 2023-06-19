from backend.generate import *
from backend.ElGamal import *

import secrets

import base64
import json


if __name__ == '__main__':
    private_key_info, public_key_info = generate_keys('name', 'email', 'ElGamal', 1024, 'passphrase')

    hash = private_key_info['private_key']

    decoded = base64.b64decode(hash).decode()

    elgamal_json = eval(decoded)


    p = elgamal_json['p']
    g = elgamal_json['g']
    y = elgamal_json['y']
    x = elgamal_json['x']

    elgamal_key_public = construct((p,g,y))

    key = secrets.token_bytes(16)
    print(key)
    message = key.hex()
    k=3

    encrypted_msg = elgamal_key_public.encrypt(message,3)

    elgamal_private_key = construct((p,g,y,x))
    
    encrypted_msg = str(encrypted_msg).encode('utf-8')

    tmp1 = base64.b64encode(encrypted_msg).decode('utf-8')

    encrypted_key = base64.b64decode(tmp1.encode('utf-8'))

    encrypted_key = eval(encrypted_key)

    decrypted_msg = elgamal_private_key.decrypt(encrypted_key)

    key_2 = bytes.fromhex(decrypted_msg)
    print(key_2)




    print(decoded)