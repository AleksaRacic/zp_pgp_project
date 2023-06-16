from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

password = b"my_password"
encryption_algorithm = serialization.BestAvailableEncryption(password)

# Generate the DSA key pair
private_key = dsa.generate_private_key(
    key_size=1024
)
public_key = private_key.public_key()

# Serialize the private key in PEM format
pem_private_key = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=encryption_algorithm
)

# Serialize the public key in PEM format
pem_public_key = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Save the keys to files
with open('private_key.pem', 'wb') as f:
    f.write(pem_private_key)

with open('public_key.pem', 'wb') as f:
    f.write(pem_public_key)

    # Load the private key from the PEM file
with open('private_key.pem', 'rb') as f:
    private_key1 = serialization.load_pem_private_key(
        f.read(),
        password=password
    )

# Sign a message
message = b'This is the message to be signed'
signature = private_key1.sign(
    message,
    hashes.SHA1()
)

signature_hex = signature.hex()

print("Signature:", signature_hex)

# Load the public key from the PEM file
with open('public_key.pem', 'rb') as f:
    public_key1 = serialization.load_pem_public_key(
        f.read()
    )

# Verify the signature
message = b'This is the message to be verified'
signature1 = bytes.fromhex(signature_hex)  # Replace '...' with the actual signature


public_key1.verify(
    signature,
    message,
    hashes.SHA1()
)
print("Signature is valid.")
#