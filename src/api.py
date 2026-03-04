from datetime import datetime, timezone
from pathlib import Path
from src.db import connect, init_db
from src.audit import log_event
from src import rbac

from src.crypto_aes import aes_keygen, aes_encrypt, aes_decrypt, AesBlob
from src.crypto_rsa import rsa_keygen, rsa_wrap, rsa_unwrap
from src.crypto_rsa import load_or_generate_rsa_keys

_RSA_KEYS = load_or_generate_rsa_keys(Path("keys/rsa_keypair.pem"))

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def login(user_id: str, role: str) -> None:
    init_db()
    log_event(user_id, role, "LOGIN", None, "User logged in (demo)")


def encrypt_and_store_record(
    user_id: str,
    role: str,
    patient_id: str,
    plaintext: bytes,
    scheme: str = "RSA-2048 + AES-256",
) -> None:
    # Zero-trust style: verify role/action
    if role == rbac.ROLE_PATIENT:
        log_event(user_id, role, "DENY_WRITE", patient_id, "Patient cannot write")
        raise PermissionError("Access denied: Patient cannot write records.")

    # RSA-only mode
    if scheme != "RSA-2048 + AES-256":
        raise ValueError("Kyber mode not available. Use RSA-2048 + AES-256.")

    # 1) Generate AES key and encrypt record (AES-256-GCM)
    aes_key = aes_keygen()
    blob = aes_encrypt(aes_key, plaintext)

    # 2) Wrap AES key using RSA public key (OAEP)
    wrapped_key = rsa_wrap(_RSA_KEYS.pub, aes_key)

    # 3) Store encrypted record + wrapped key
    con = connect()
    try:
        with con:
            con.execute(
                "INSERT INTO medical_records(patient_id, created_by, scheme, nonce, ciphertext, wrapped_key, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (patient_id, user_id, scheme, blob.nonce, blob.ciphertext, wrapped_key, _now_iso()),
            )
        log_event(user_id, role, "WRITE_RECORD", patient_id, f"Stored record using {scheme}")
    finally:
        con.close()


def fetch_and_decrypt_records(user_id: str, role: str, patient_id: str) -> list[bytes]:
    # Zero-trust: RBAC check before data access
    if not rbac.can_view(role, user_id, patient_id):
        log_event(user_id, role, "DENY_READ", patient_id, "RBAC denied read")
        raise PermissionError("Access denied: cannot view this patient.")

    con = connect()
    try:
        rows = con.execute(
            "SELECT nonce, ciphertext, wrapped_key, scheme FROM medical_records WHERE patient_id=? ORDER BY created_at DESC",
            (patient_id,),
        ).fetchall()
    finally:
        con.close()

    out: list[bytes] = []
    for row in rows:
        scheme = row["scheme"]
        if scheme != "RSA-2048 + AES-256":
            continue

        wrapped_key = row["wrapped_key"]
        blob = AesBlob(nonce=row["nonce"], ciphertext=row["ciphertext"])

        # 1) Unwrap AES key with RSA private key
        aes_key = rsa_unwrap(_RSA_KEYS.priv, wrapped_key)

        # 2) Decrypt ciphertext
        out.append(aes_decrypt(aes_key, blob))

    log_event(user_id, role, "READ_RECORD", patient_id, f"Decrypted {len(out)} record(s)")
    return out