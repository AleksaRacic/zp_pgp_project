import time
import json
import zlib
import base64
import secrets

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

from Crypto.Cipher import DES3, AES
from Crypto.Util.Padding import pad

class SendMessageBuilder:

    def __init__(self, plain_text, subject):
        self.plain_message={
            'subject' : subject,
            'timestamp' : time.time(),
            'message' : plain_text
        }

        self.message = json.dumps(self.plain_message).encode('utf-8')

    
    def sign(self, private_key, password, private_key_id):

        encoded_pk = private_key.encode('utf-8')

        private_key_object = serialization.load_pem_private_key(
            encoded_pk,
            password=password.encode('utf-8')
        )
        
        signature = private_key_object.sign(
            self.message,
            hashes.SHA1()
        )

        self.signature_json = {
            'message_digest' : signature.hex(),
            'key_id' : private_key_id,
            'timestamp' : time.time()
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
    
    def encrypt(self, algorithm, public_key, public_key_id):
        key = secrets.token_bytes(16)

        encoded_pk = public_key.encode('utf-8')

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
            'encrypted_key' : encrypted_key.decode('utf-8'),
            algorithm : encrypted_message.decode('utf-8'),
            'key_id' : public_key_id
        }

        self.message = json.dumps(self.message).encode('utf-8')
        return self


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
    
    def verify_signature(self, public_key):
        encoded_pk = public_key.encode('utf-8')

        public_key_object = serialization.load_pem_public_key(
            encoded_pk
        )

        msg_json = json.loads(self.message.decode('utf-8'))

        signature = bytes.fromhex(msg_json['signature']['message_digest'])

        message = msg_json['message'].encode('utf-8')

        try:
            public_key_object.verify(
            signature,
            message,
            hashes.SHA1()
            )   
            return True
        except InvalidSignature:
            return False


    

    