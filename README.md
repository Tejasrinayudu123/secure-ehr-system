# Secure EHR System with Post-Quantum Cryptography

A demo Electronic Health Record (EHR) backend that uses post-quantum cryptography for secure key establishment and digital signatures. The project combines **ML-KEM-768** (the NIST-standardized form of CRYSTALS-Kyber), **ML-DSA-65** (the NIST-standardized form of CRYSTALS-Dilithium), and **AES-256-GCM** for encrypted patient record handling. NIST finalized ML-KEM in FIPS 203 and ML-DSA in FIPS 204 in August 2024, and the current `pqcrypto` package exposes these standardized algorithm names directly. citeturn477623search0turn477623search1turn493707view0

## Project Status

Implemented now:
- ML-KEM-768 key generation, encapsulation, and decapsulation
- ML-DSA-65 key generation, signing, and verification
- AES-256-GCM encryption and decryption for EHR payloads
- FastAPI endpoints for key generation, record encryption/decryption, and signature verification
- JSON-based API requests and responses using Pydantic models, which aligns with FastAPI's recommended request-body pattern. citeturn493707view1turn446490search5

Planned next:
- Database integration for persistent record storage
- JWT authentication and RBAC
- Audit logging
- Frontend dashboard for doctors, admins, and patients

## Algorithms Used

| Layer | Algorithm | Purpose |
|---|---|---|
| Key encapsulation | ML-KEM-768 | Shared secret generation |
| Digital signature | ML-DSA-65 | Integrity and authentication |
| Symmetric encryption | AES-256-GCM | Encrypt EHR content |

## Why the Code Uses ML-KEM and ML-DSA Names

Older project descriptions often say **Kyber** and **Dilithium**, but the NIST-standardized names are now **ML-KEM** and **ML-DSA**. This is why the Python imports in this implementation use:

- `pqcrypto.kem.ml_kem_768`
- `pqcrypto.sign.ml_dsa_65`

That naming matches the currently published standards and the latest `pqcrypto` release. citeturn477623search0turn477623search1turn493707view0

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Tejasrinayudu123/secure-ehr-system.git
cd secure-ehr-system
```

### 2. Create and activate a virtual environment

**Windows**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the API

```bash
uvicorn src.api:app --reload
```

After the server starts, open:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

FastAPI automatically generates interactive API docs from your request/response models. citeturn493707view1turn446490search22

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/health` | Health check |
| GET | `/keys/kem` | Generate ML-KEM key pair |
| GET | `/keys/sign` | Generate ML-DSA key pair |
| POST | `/encrypt_record` | Encrypt a patient record |
| POST | `/decrypt_record` | Decrypt a patient record |
| POST | `/sign_data` | Sign a message |
| POST | `/verify_signature` | Verify a signature |

## Example 1: Generate KEM Keys

### Request
```bash
curl -X GET "http://127.0.0.1:8000/keys/kem"
```

### Example Response
```json
{
  "public_key_b64": "BASE64_PUBLIC_KEY",
  "secret_key_b64": "BASE64_SECRET_KEY"
}
```

## Example 2: Encrypt an EHR Record

### Request
```bash
curl -X POST "http://127.0.0.1:8000/encrypt_record" \
  -H "Content-Type: application/json" \
  -d '{
    "public_key_b64": "BASE64_PUBLIC_KEY",
    "patient_id": "P1001",
    "patient_name": "John Doe",
    "diagnosis": "Hypertension",
    "prescription": "Amlodipine 5mg"
  }'
```

### Example Response
```json
{
  "kem_ciphertext_b64": "BASE64_KEM_CIPHERTEXT",
  "shared_secret_b64": "BASE64_SHARED_SECRET",
  "aes_nonce_b64": "BASE64_NONCE",
  "encrypted_record_b64": "BASE64_AES_CIPHERTEXT",
  "plaintext_preview": "{\"patient_id\": \"P1001\", \"patient_name\": \"John Doe\", \"diagnosis\": \"Hypertension\", \"prescription\": \"Amlodipine 5mg\"}"
}
```

## Example 3: Decrypt an EHR Record

### Request
```bash
curl -X POST "http://127.0.0.1:8000/decrypt_record" \
  -H "Content-Type: application/json" \
  -d '{
    "secret_key_b64": "BASE64_SECRET_KEY",
    "kem_ciphertext_b64": "BASE64_KEM_CIPHERTEXT",
    "aes_nonce_b64": "BASE64_NONCE",
    "encrypted_record_b64": "BASE64_AES_CIPHERTEXT"
  }'
```

### Example Response
```json
{
  "record_json": "{\"patient_id\": \"P1001\", \"patient_name\": \"John Doe\", \"diagnosis\": \"Hypertension\", \"prescription\": \"Amlodipine 5mg\"}"
}
```

## Example 4: Generate Signature Keys

### Request
```bash
curl -X GET "http://127.0.0.1:8000/keys/sign"
```

### Example Response
```json
{
  "public_key_b64": "BASE64_SIGN_PUBLIC_KEY",
  "secret_key_b64": "BASE64_SIGN_SECRET_KEY"
}
```

## Example 5: Sign Data

### Request
```bash
curl -X POST "http://127.0.0.1:8000/sign_data" \
  -H "Content-Type: application/json" \
  -d '{
    "secret_key_b64": "BASE64_SIGN_SECRET_KEY",
    "message": "patient_id=P1001|diagnosis=Hypertension"
  }'
```

### Example Response
```json
{
  "signature_b64": "BASE64_SIGNATURE"
}
```

## Example 6: Verify Signature

### Request
```bash
curl -X POST "http://127.0.0.1:8000/verify_signature" \
  -H "Content-Type: application/json" \
  -d '{
    "public_key_b64": "BASE64_SIGN_PUBLIC_KEY",
    "message": "patient_id=P1001|diagnosis=Hypertension",
    "signature_b64": "BASE64_SIGNATURE"
  }'
```

### Example Response
```json
{
  "is_valid": true
}
```

## Security Notes

This project is a learning and prototype implementation. In production, do not:
- return shared secrets to clients in API responses
- store private keys in plaintext
- rely on demo-only request flows
- skip authentication, authorization, and audit logging

A production design should generate and protect keys in secure key stores or HSM-backed services, authenticate all users, and persist encrypted records in a real database.

## References

- NIST FIPS 203: ML-KEM standard. citeturn477623search0turn477623search4
- NIST FIPS 204: ML-DSA standard. citeturn477623search1turn477623search3
- NIST PQC project overview. citeturn477623search8turn477623search5
- `pqcrypto` 0.4.0 package and supported algorithm names. citeturn493707view0
- FastAPI request body and response model documentation. citeturn493707view1turn446490search5
