import datetime
import json
import zlib
import base64
import secrets

from .ElGamal import *

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

from Crypto.Cipher import DES3, AES
from Crypto.Util.Padding import pad, unpad

class SendMessageBuilder:

    def __init__(self, plain_text, subject, sender):
        self.plain_message={
            'subject' : subject,
            'timestamp' : datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
            'message' : plain_text,
            'sender' : sender
        }

        self.message = json.dumps(self.plain_message).encode('utf-8')

    
    def sign(self, private_key, password, private_key_id, private_key_algorithm):

        encoded_pk = private_key.encode('utf-8')

        private_key_object = serialization.load_pem_private_key(
            encoded_pk,
            password=password.encode('utf-8')
        )

        if private_key_algorithm == 'RSA':
            signature = private_key_object.sign(
                self.message,
                padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA1()
            )
        elif private_key_algorithm == 'DSA':
            signature = private_key_object.sign(
                self.message,
                hashes.SHA1()
            )
        elif private_key_algorithm == 'ElGamal':
            raise Exception
        else:
            raise Exception
        
        self.signature_json = {
            'message_digest' : signature.hex(),
            'key_id' : private_key_id,
            'timestamp' : datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
            'algorithm' : private_key_algorithm
        }

        self.message = {
            'signature' : self.signature_json,
            'message' : self.message.decode('utf-8')
        }

        self.message = json.dumps(self.message).encode('utf-8')

        return self
    
    def zip(self):
        self.message = zlib.compress(self.message)
        self.message = {
            'zip' : base64.b64encode(self.message).decode('utf-8')
        }
        self.message = json.dumps(self.message).encode('utf-8')
        return self
    
    def encrypt(self, algorithm, public_key, public_key_id, public_key_algorithm):
        key = secrets.token_bytes(16)

        encoded_pk = public_key.encode('utf-8')

        if public_key_algorithm == 'RSA':
            public_key_object = serialization.load_pem_public_key(
                encoded_pk,
                backend=default_backend()
            )
            encrypted_key = public_key_object.encrypt(
                key,
                padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
            )
        elif public_key_algorithm == 'ElGamal':
            decoded_key = base64.b64decode(public_key).decode()
            elgamal_json = eval(decoded_key)
            p = elgamal_json['p']
            g = elgamal_json['g']
            y = elgamal_json['y']
            elgamal_key_public = construct((p,g,y))
            encrypted_key = elgamal_key_public.encrypt(key.hex(),3)
            encrypted_key = str(encrypted_key).encode('utf-8')

        else:
            raise Exception('Unsupported algorithm')
        
        algo_object = None
        if algorithm == 'DES3':
            algo_object = DES3
        elif algorithm == 'AES':
            algo_object = AES
        else:
            raise Exception('Algorithm not supported')
        
        padded_message = pad(self.message, algo_object.block_size)
        cipher = algo_object.new(key, algo_object.MODE_ECB)

        encrypted_message = cipher.encrypt(padded_message)

        self.message = {
            'encrypted_key' : base64.b64encode(encrypted_key).decode('utf-8'),
            algorithm : base64.b64encode(encrypted_message).decode('utf-8'),
            'key_id' : public_key_id,
            'key_algorithm' : public_key_algorithm
        }

        self.message = json.dumps(self.message).encode('utf-8')
        return self
    
    def to_base64(self):
        self.message = {
            'base64' : self.message.decode('utf-8')
        }
        self.message = base64.b64encode(json.dumps(self.message).encode('utf-8'))

    def build(self):
        return self.message
    

    
class ReceiveMsgBuilder:
    
    def __init__(self, message):
        self.message = message

    def check_zip(self):
        msg_json = json.loads(self.message.decode('utf-8'))
        if msg_json.get("zip") is None:
            return False
        return True
    
    def unzip(self):
        msg_json = json.loads(self.message.decode('utf-8'))
        msg1 = msg_json['zip'].encode('utf-8')
        msg1 = base64.b64decode(msg1)
        self.message = zlib.decompress(msg1)
    
    def is_signed(self):
        msg_json = json.loads(self.message.decode('utf-8'))
        if msg_json.get("signature") is None:
            return False
        return True
    
    def get_signature_key_id(self):
        msg_json = json.loads(self.message.decode('utf-8'))
        return msg_json['signature']['key_id']
    
    def remove_signature(self):
        msg_json = json.loads(self.message.decode('utf-8'))
        self.message = msg_json['message'].encode('utf-8')
    
    def verify_signature(self, public_key):
        encoded_pk = public_key.encode('utf-8')

        public_key_object = serialization.load_pem_public_key(
            encoded_pk
        )

        msg_json = json.loads(self.message.decode('utf-8'))

        signature = bytes.fromhex(msg_json['signature']['message_digest'])

        message = msg_json['message'].encode('utf-8')

        algorithm = msg_json['signature']['algorithm']

        try:
            if algorithm == 'RSA':
                public_key_object.verify(
                signature,
                message,
                padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA1()
                )   
                return True
            elif algorithm == 'DSA':
                public_key_object.verify(
                signature,
                message,
                hashes.SHA1()
                )
                return True
            return False
        except InvalidSignature:
            return False
    
    def is_encripted(self):
        msg_json = json.loads(self.message.decode('utf-8'))
        if msg_json.get("encrypted_key") is None:
            return False
        return True

    def get_encription_key_id(self):
        msg_json = json.loads(self.message.decode('utf-8'))
        return msg_json['key_id']
    
    def decrypt(self, private_key, password):
        msg_json = json.loads(self.message.decode('utf-8'))

        if msg_json.get("DES3") is not None:
            algo_object = DES3
            algorithm_s='DES3'
        elif msg_json.get("AES") is not None:
            algo_object = AES
            algorithm_s='AES'
        else:
            raise Exception('Unsupported algorithm')
        
        encrypted_key = base64.b64decode(msg_json['encrypted_key'].encode('utf-8'))

        if msg_json['key_algorithm'] == 'RSA':
            encoded_pk = private_key.encode('utf-8')
            private_key_object = serialization.load_pem_private_key(
            encoded_pk,
            password=password.encode('utf-8')
            )

            
            decrypted_key = private_key_object.decrypt(
                encrypted_key,
                padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
            )
        elif True: 
            decoded_key = base64.b64decode(private_key).decode()
            elgamal_json = eval(decoded_key)
            p = elgamal_json['p']
            g = elgamal_json['g']
            y = elgamal_json['y']
            x = elgamal_json['x']
            elgamal_key_public = construct((p,g,y,x))
            encrypted_key_elgamal = eval(encrypted_key)
            decrypted_msg = elgamal_key_public.decrypt(encrypted_key_elgamal)
            decrypted_key = bytes.fromhex(decrypted_msg)
        else:
            raise Exception('Unsupported algorithm')
        
        encrypted_message = base64.b64decode(msg_json[algorithm_s].encode('utf-8'))
        cipher = algo_object.new(decrypted_key, algo_object.MODE_ECB)
        self.message = unpad(cipher.decrypt(encrypted_message), algo_object.block_size)
    
    def is_base64(self):
        try:
            decoded_data = base64.b64decode(self.message)
            data_json = json.loads(decoded_data.decode('utf-8'))
            if data_json.get('base64') is None:
                return False
            return True
        except Exception:
            return False
        
    def decode_base64(self):
        decoded_data = base64.b64decode(self.message)
        data_json = json.loads(decoded_data.decode('utf-8'))
        self.message = data_json['base64'].encode('utf-8')

    
    def build(self):
        return json.loads(self.message.decode('utf-8'))

        


    

    