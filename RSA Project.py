import cryptography
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

def generate_keys():
    # Generate RSA Key Pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Serialize and store keys
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Write private key to a file
    with open('private_key.pem', 'wb') as f:
        f.write(private_pem)

    # Write public key to a file
    with open('public_key.pem', 'wb') as f:
        f.write(public_pem)

def encrypt_file(input_file, output_file):

    # Open the input file
    with open(input_file, 'rb') as f:
        plaintext = f.read()

    # Open the public key
    with open('public_key.pem', 'rb') as f:
        public_pem = f.read()
        public_key = serialization.load_pem_public_key(public_pem,
        backend=default_backend())

    #Encrypt the plaintext
    ciphertext = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Write the output file as ciphertext
    with open(output_file, 'wb') as f:
        f.write(ciphertext)

def decrypt_file(input_file, output_file):

    # Open the input (ciphertext) file
    with open(input_file, 'rb') as f:
        ciphertext = f.read()

    # Open the private key file
    with open('private_key.pem', 'rb') as f:
        private_pem = f.read()
        private_key = serialization.load_pem_private_key(private_pem,
        password=None, backend=default_backend())

    # Decrypt the ciphertext
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Write the decrypted message to an output file
    with open(output_file, 'wb') as f:
        f.write(plaintext)

# Generate RSA key pair
generate_keys()

# Encrypt text file
encrypt_file('Hidden Message.txt', 'encrypted_message.txt')

# Decrypt text file
decrypt_file('encrypted_message.txt', 'decrypted_message.txt')