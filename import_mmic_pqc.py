import json
from src.db import init_db
from src.api import login, encrypt_and_store_record
from src.mimic_loader import load_ehr_payloads

def main():
    init_db()
    login("doctor1", "Doctor")

    scheme = "ML-KEM-768 + AES-256"
    payloads = load_ehr_payloads(limit=50)

    count = 0
    for p in payloads:
        plaintext = json.dumps(p, ensure_ascii=False).encode("utf-8")

        encrypt_and_store_record(
            user_id="doctor1",
            role="Doctor",
            patient_id=p["patient_id"],
            plaintext=plaintext,
            scheme=scheme
        )
        count += 1

    print(f"✅ Imported + encrypted {count} records using {scheme}")

if __name__ == "__main__":
    main()