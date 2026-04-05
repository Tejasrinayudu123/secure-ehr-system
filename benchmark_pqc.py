import json
import time
import statistics as stats

from src.api import login, encrypt_and_store_record, fetch_and_decrypt_records
from src.mimic_loader import load_ehr_payloads


def benchmark_scheme(scheme: str, limit: int = 30):
    login("doctor1", "Doctor")
    payloads = load_ehr_payloads(limit=limit)

    enc_times = []
    for p in payloads:
        plaintext = json.dumps(p, ensure_ascii=False).encode("utf-8")

        t0 = time.perf_counter()
        encrypt_and_store_record(
            user_id="doctor1",
            role="Doctor",
            patient_id=p["patient_id"],
            plaintext=plaintext,
            scheme=scheme,
        )
        t1 = time.perf_counter()
        enc_times.append((t1 - t0) * 1000.0)

    pid = payloads[0]["patient_id"]
    t0 = time.perf_counter()
    records = fetch_and_decrypt_records("doctor1", "Doctor", pid)
    t1 = time.perf_counter()
    dec_time = (t1 - t0) * 1000.0

    print(f"\n=== {scheme} ===")
    print(f"Records encrypted: {len(payloads)}")
    print(f"Mean encryption time (ms): {stats.mean(enc_times):.3f}")
    print(f"Std encryption time (ms): {stats.pstdev(enc_times):.3f}")
    print(f"Decryption time (ms): {dec_time:.3f}")
    print(f"Sample decrypted records: {len(records)}")


if __name__ == "__main__":
    benchmark_scheme("RSA-2048 + AES-256", limit=30)
    benchmark_scheme("ML-KEM-768 + AES-256", limit=30)