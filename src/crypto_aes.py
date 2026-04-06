from __future__ import annotations

import base64
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def encrypt_record(plaintext: bytes, key: bytes) -> dict[str, str]:
    """Encrypt bytes with AES-256-GCM.

    Returns base64-encoded nonce and ciphertext for JSON-friendly transport.
    """
    if len(key) != 32:
        raise ValueError("AES key must be exactly 32 bytes for AES-256-GCM.")

    nonce = os.urandom(12)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    return {
        "nonce_b64": base64.b64encode(nonce).decode("utf-8"),
        "ciphertext_b64": base64.b64encode(ciphertext).decode("utf-8"),
    }


def decrypt_record(nonce_b64: str, ciphertext_b64: str, key: bytes) -> bytes:
    """Decrypt AES-256-GCM encrypted data."""
    if len(key) != 32:
        raise ValueError("AES key must be exactly 32 bytes for AES-256-GCM.")

    nonce = base64.b64decode(nonce_b64)
    ciphertext = base64.b64decode(ciphertext_b64)
    aesgcm = AESGCM(key)

    return aesgcm.decrypt(nonce, ciphertext, None)
