from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

def hkdf_32(shared_secret: bytes, salt: bytes = b"", info: bytes = b"ehr-demo") -> bytes:
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt or None,
        info=info
    )
    return hkdf.derive(shared_secret)