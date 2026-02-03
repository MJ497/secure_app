import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

KEY_SIZE = 32   # 256 bits
NONCE_SIZE = 12 # 96 bits (recommended for GCM)


def generate_key() -> bytes:
    """
    Generates a secure random 256-bit AES key.
    """
    return os.urandom(KEY_SIZE)


def encrypt_data(key: bytes, plaintext: bytes) -> bytes:
    """
    Encrypts data using AES-GCM.
    Returns: nonce + ciphertext
    """
    aesgcm = AESGCM(key)
    nonce = os.urandom(NONCE_SIZE)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return nonce + ciphertext


def decrypt_data(key: bytes, encrypted: bytes) -> bytes:
    """
    Decrypts AES-GCM encrypted data.
    """
    nonce = encrypted[:NONCE_SIZE]
    ciphertext = encrypted[NONCE_SIZE:]
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None)
