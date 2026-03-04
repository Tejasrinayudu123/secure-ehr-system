import os
from dataclasses import dataclass
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

@dataclass
class AesBlob:
    nonce: bytes
    ciphertext: bytes

def aes_keygen() -> bytes:
    return os.urandom(32)  # AES-256

def aes_encrypt(key: bytes, plaintext: bytes, aad: bytes = b"ehr") -> AesBlob:
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, plaintext, aad)
    return AesBlob(nonce=nonce, ciphertext=ct)

def aes_decrypt(key: bytes, blob: AesBlob, aad: bytes = b"ehr") -> bytes:
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(blob.nonce, blob.ciphertext, aad)