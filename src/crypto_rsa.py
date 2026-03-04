from dataclasses import dataclass
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization


@dataclass
class RsaKeyPair:
    priv: rsa.RSAPrivateKey
    pub: rsa.RSAPublicKey


def rsa_keygen(bits: int = 2048) -> RsaKeyPair:
    priv = rsa.generate_private_key(public_exponent=65537, key_size=bits)
    return RsaKeyPair(priv=priv, pub=priv.public_key())


def rsa_wrap(pub: rsa.RSAPublicKey, key: bytes) -> bytes:
    return pub.encrypt(
        key,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def rsa_unwrap(priv: rsa.RSAPrivateKey, wrapped: bytes) -> bytes:
    return priv.decrypt(
        wrapped,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def load_or_generate_rsa_keys(pem_path: Path, bits: int = 2048) -> RsaKeyPair:
    """
    Persist RSA keys to disk so encryption + decryption always use the same keypair.
    Stores private key in PEM format; public key is derived from it.
    """
    pem_path.parent.mkdir(parents=True, exist_ok=True)

    if pem_path.exists():
        pem_bytes = pem_path.read_bytes()
        priv = serialization.load_pem_private_key(pem_bytes, password=None)
        assert isinstance(priv, rsa.RSAPrivateKey)
        return RsaKeyPair(priv=priv, pub=priv.public_key())

    keys = rsa_keygen(bits)
    pem_bytes = keys.priv.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    pem_path.write_bytes(pem_bytes)
    return keys