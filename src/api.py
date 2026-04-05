from datetime import datetime, timezone
from pathlib import Path

from src.db import connect, init_db
from src.audit import log_event
from src import rbac

from src.crypto_aes import aes_keygen, aes_encrypt, aes_decrypt, AesBlob
from src.crypto_rsa import load_or_generate_rsa_keys, rsa_wrap, rsa_unwrap
from src.crypto_pqc import (
    mlkem_keygen,
    mlkem_encapsulate,
    mlkem_decapsulate,
    mldsa_keygen,
    mldsa_sign,
    mldsa_verify,
)

# Persistent RSA keys
_RSA_KEYS = load_or_generate_rsa_keys(Path("keys/rsa_keypair.pem"))

# In-memory PQC keys for prototype use
_PQC_KEM_KEYS = mlkem_keygen()
_PQC_SIG_KEYS = mldsa_keygen()


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
    if role == rbac.ROLE_PATIENT:
        log_event(user_id, role, "DENY_WRITE", patient_id, "Patient cannot write")
        raise PermissionError("Access denied: Patient cannot write records.")

    sig_alg = None
    signature = None
    sig_public_key = None

    if scheme == "RSA-2048 + AES-256":
        aes_key = aes_keygen()
        blob = aes_encrypt(aes_key, plaintext)
        wrapped_key = rsa_wrap(_RSA_KEYS.pub, aes_key)

    elif scheme == "ML-KEM-768 + AES-256":
        kem_ciphertext, shared_secret = mlkem_encapsulate(_PQC_KEM_KEYS.public_key)
        aes_key = shared_secret[:32]  # 32 bytes for AES-256
        blob = aes_encrypt(aes_key, plaintext)
        wrapped_key = kem_ciphertext

        sig_alg = "ML-DSA-65"
        signature = mldsa_sign(_PQC_SIG_KEYS.sig, blob.ciphertext)
        sig_public_key = _PQC_SIG_KEYS.public_key

    else:
        raise ValueError("Unsupported scheme")

    con = connect()
    try:
        with con:
            con.execute(
                """
                INSERT INTO medical_records
                (patient_id, created_by, scheme, nonce, ciphertext, wrapped_key, sig_alg, signature, sig_public_key, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    patient_id,
                    user_id,
                    scheme,
                    blob.nonce,
                    blob.ciphertext,
                    wrapped_key,
                    sig_alg,
                    signature,
                    sig_public_key,
                    _now_iso(),
                ),
            )
        log_event(user_id, role, "WRITE_RECORD", patient_id, f"Stored record using {scheme}")
    finally:
        con.close()


def fetch_and_decrypt_records(user_id: str, role: str, patient_id: str) -> list[bytes]:
    if not rbac.can_view(role, user_id, patient_id):
        log_event(user_id, role, "DENY_READ", patient_id, "RBAC denied read")
        raise PermissionError("Access denied: cannot view this patient.")

    con = connect()
    try:
        rows = con.execute(
            """
            SELECT nonce, ciphertext, wrapped_key, scheme, sig_alg, signature, sig_public_key
            FROM medical_records
            WHERE patient_id=?
            ORDER BY created_at DESC
            """,
            (patient_id,),
        ).fetchall()
    finally:
        con.close()

    out: list[bytes] = []

    for row in rows:
        scheme = row["scheme"]
        blob = AesBlob(nonce=row["nonce"], ciphertext=row["ciphertext"])

        if scheme == "RSA-2048 + AES-256":
            aes_key = rsa_unwrap(_RSA_KEYS.priv, row["wrapped_key"])

        elif scheme == "ML-KEM-768 + AES-256":
            if row["signature"] is None or row["sig_public_key"] is None:
                raise ValueError("Missing ML-DSA signature data")
            ok = mldsa_verify(row["sig_public_key"], row["ciphertext"], row["signature"])
            if not ok:
                raise ValueError("ML-DSA signature verification failed")
            shared_secret = mlkem_decapsulate(_PQC_KEM_KEYS.kem, row["wrapped_key"])
            aes_key = shared_secret[:32]

        else:
            continue

        plaintext = aes_decrypt(aes_key, blob)
        out.append(plaintext)

    log_event(user_id, role, "READ_RECORD", patient_id, f"Decrypted {len(out)} record(s)")
    return out