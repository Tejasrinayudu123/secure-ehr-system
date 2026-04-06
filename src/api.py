from __future__ import annotations

import base64
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.crypto_aes import encrypt_record, decrypt_record
from src.crypto_kyber import (
    generate_ml_kem_keypair,
    encapsulate_shared_secret,
    decapsulate_shared_secret,
)
from src.crypto_dilithium import (
    generate_ml_dsa_keypair,
    sign_message,
    verify_message,
)

app = FastAPI(
    title="Secure EHR System API",
    version="1.0.0",
    description=(
        "A demo Electronic Health Record backend using "
        "ML-KEM-768 (Kyber), ML-DSA-65 (Dilithium), and AES-256-GCM."
    ),
)


class EncryptRecordRequest(BaseModel):
    public_key_b64: str = Field(..., description="Recipient ML-KEM public key in Base64.")
    patient_id: str
    patient_name: str
    diagnosis: str
    prescription: str


class EncryptRecordResponse(BaseModel):
    kem_ciphertext_b64: str
    shared_secret_b64: str
    aes_nonce_b64: str
    encrypted_record_b64: str
    plaintext_preview: str


class DecryptRecordRequest(BaseModel):
    secret_key_b64: str = Field(..., description="Recipient ML-KEM secret key in Base64.")
    kem_ciphertext_b64: str
    aes_nonce_b64: str
    encrypted_record_b64: str


class DecryptRecordResponse(BaseModel):
    record_json: str


class SignRequest(BaseModel):
    secret_key_b64: str
    message: str


class SignResponse(BaseModel):
    signature_b64: str


class VerifyRequest(BaseModel):
    public_key_b64: str
    message: str
    signature_b64: str


class VerifyResponse(BaseModel):
    is_valid: bool


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Secure EHR System API is running."}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/keys/kem")
def create_kem_keys() -> dict[str, str]:
    return generate_ml_kem_keypair()


@app.get("/keys/sign")
def create_sign_keys() -> dict[str, str]:
    return generate_ml_dsa_keypair()


@app.post("/encrypt_record", response_model=EncryptRecordResponse)
def encrypt_record_endpoint(payload: EncryptRecordRequest) -> EncryptRecordResponse:
    record_json = (
        "{"
        f"\"patient_id\": \"{payload.patient_id}\", "
        f"\"patient_name\": \"{payload.patient_name}\", "
        f"\"diagnosis\": \"{payload.diagnosis}\", "
        f"\"prescription\": \"{payload.prescription}\""
        "}"
    )

    kem_result = encapsulate_shared_secret(payload.public_key_b64)
    aes_key = base64.b64decode(kem_result["shared_secret_b64"])

    aes_result = encrypt_record(record_json.encode("utf-8"), aes_key)

    return EncryptRecordResponse(
        kem_ciphertext_b64=kem_result["ciphertext_b64"],
        shared_secret_b64=kem_result["shared_secret_b64"],
        aes_nonce_b64=aes_result["nonce_b64"],
        encrypted_record_b64=aes_result["ciphertext_b64"],
        plaintext_preview=record_json,
    )


@app.post("/decrypt_record", response_model=DecryptRecordResponse)
def decrypt_record_endpoint(payload: DecryptRecordRequest) -> DecryptRecordResponse:
    try:
        shared_secret = decapsulate_shared_secret(
            payload.secret_key_b64,
            payload.kem_ciphertext_b64,
        )
        aes_key = base64.b64decode(shared_secret["shared_secret_b64"])
        plaintext = decrypt_record(
            payload.aes_nonce_b64,
            payload.encrypted_record_b64,
            aes_key,
        ).decode("utf-8")

        return DecryptRecordResponse(record_json=plaintext)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Decryption failed: {exc}") from exc


@app.post("/sign_data", response_model=SignResponse)
def sign_data(payload: SignRequest) -> SignResponse:
    try:
        result = sign_message(payload.secret_key_b64, payload.message)
        return SignResponse(signature_b64=result["signature_b64"])
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Signing failed: {exc}") from exc


@app.post("/verify_signature", response_model=VerifyResponse)
def verify_signature(payload: VerifyRequest) -> VerifyResponse:
    try:
        valid = verify_message(
            payload.public_key_b64,
            payload.message,
            payload.signature_b64,
        )
        return VerifyResponse(is_valid=valid)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Verification failed: {exc}") from exc
