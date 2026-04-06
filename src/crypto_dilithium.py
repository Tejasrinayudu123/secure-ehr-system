from __future__ import annotations

import base64
from pqcrypto.sign.ml_dsa_65 import generate_keypair, sign, verify


def generate_ml_dsa_keypair() -> dict[str, str]:
    """Generate an ML-DSA-65 keypair (standardized form of CRYSTALS-Dilithium)."""
    public_key, secret_key = generate_keypair()
    return {
        "public_key_b64": base64.b64encode(public_key).decode("utf-8"),
        "secret_key_b64": base64.b64encode(secret_key).decode("utf-8"),
    }


def sign_message(secret_key_b64: str, message: str) -> dict[str, str]:
    """Sign a UTF-8 message with ML-DSA-65."""
    secret_key = base64.b64decode(secret_key_b64)
    signature = sign(secret_key, message.encode("utf-8"))

    return {"signature_b64": base64.b64encode(signature).decode("utf-8")}


def verify_message(public_key_b64: str, message: str, signature_b64: str) -> bool:
    """Verify a UTF-8 message signature with ML-DSA-65."""
    public_key = base64.b64decode(public_key_b64)
    signature = base64.b64decode(signature_b64)
    return bool(verify(public_key, message.encode("utf-8"), signature))
