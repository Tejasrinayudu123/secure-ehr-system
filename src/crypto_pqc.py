from dataclasses import dataclass
import oqs

MLKEM_ALG = "ML-KEM-768"
MLDSA_ALG = "ML-DSA-65"


@dataclass
class PQCKEMKeyPair:
    public_key: bytes
    kem: oqs.KeyEncapsulation


@dataclass
class PQCSigKeyPair:
    public_key: bytes
    sig: oqs.Signature


def mlkem_keygen() -> PQCKEMKeyPair:
    kem = oqs.KeyEncapsulation(MLKEM_ALG)
    public_key = kem.generate_keypair()
    return PQCKEMKeyPair(public_key=public_key, kem=kem)


def mlkem_encapsulate(public_key: bytes) -> tuple[bytes, bytes]:
    with oqs.KeyEncapsulation(MLKEM_ALG) as kem:
        ciphertext, shared_secret = kem.encap_secret(public_key)
    return ciphertext, shared_secret


def mlkem_decapsulate(kem: oqs.KeyEncapsulation, ciphertext: bytes) -> bytes:
    return kem.decap_secret(ciphertext)


def mldsa_keygen() -> PQCSigKeyPair:
    sig = oqs.Signature(MLDSA_ALG)
    public_key = sig.generate_keypair()
    return PQCSigKeyPair(public_key=public_key, sig=sig)


def mldsa_sign(sig: oqs.Signature, message: bytes) -> bytes:
    return sig.sign(message)


def mldsa_verify(public_key: bytes, message: bytes, signature: bytes) -> bool:
    with oqs.Signature(MLDSA_ALG) as sig:
        return sig.verify(message, signature, public_key)