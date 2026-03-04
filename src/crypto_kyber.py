from dataclasses import dataclass
from pqcrypto import kem

@dataclass
class KyberKeyPair:
    pk: bytes
    sk: bytes


def _get_impl():
    candidates = [
        "mlkem768",
        "ml_kem_768",
        "kyber768",
        "kyber_768",
        "mlkem512",
        "kyber512",
        "mlkem1024",
        "kyber1024",
    ]

    for name in candidates:
        if hasattr(kem, name):
            return getattr(kem, name)

    raise ImportError("No Kyber implementation found")


_KEM = _get_impl()


def kyber_keygen():
    pk, sk = _KEM.generate_keypair()
    return KyberKeyPair(pk, sk)


def kyber_encapsulate(pk):
    ct, ss = _KEM.encrypt(pk)
    return ct, ss


def kyber_decapsulate(ct, sk):
    return _KEM.decrypt(ct, sk)