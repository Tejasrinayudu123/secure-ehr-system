from __future__ import annotations

import base64
from pqcrypto.kem.ml_kem_768 import generate_keypair, encrypt, decrypt


def generate_ml_kem_keypair() -> dict[str, str]:
    """Generate an ML-KEM-768 keypair (standardized form of CRYSTALS-Kyber)."""
    public_key, secret_key = generate_keypair()
    return {
        "public_key_b64": base64.b64encode(public_key).decode("utf-8"),
        "secret_key_b64": base64.b64encode(secret_key).decode("utf-8"),
    }


def encapsulate_shared_secret(public_key_b64: str) -> dict[str, str]:
    """Encapsulate a shared secret using the recipient's public key."""
    public_key = base64.b64decode(public_key_b64)
    ciphertext, shared_secret = encrypt(public_key)

    return {
        "ciphertext_b64": base64.b64encode(ciphertext).decode("utf-8"),
        "shared_secret_b64": base64.b64encode(shared_secret).decode("utf-8"),
    }


def decapsulate_shared_secret(secret_key_b64: str, ciphertext_b64: str) -> dict[str, str]:
    """Recover the shared secret from the ciphertext using the secret key."""
    secret_key = base64.b64decode(secret_key_b64)
    ciphertext = base64.b64decode(ciphertext_b64)
    shared_secret = decrypt(secret_key, ciphertext)

    return {"shared_secret_b64": base64.b64encode(shared_secret).decode("utf-8")}
