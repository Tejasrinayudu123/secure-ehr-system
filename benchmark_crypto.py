import json
import time
import statistics as stats

from src.api import login, encrypt_and_store_record, fetch_and_decrypt_records
from src.mimic_loader import load_ehr_payloads


def main():
    login("doctor1", "Doctor")

    scheme = "RSA-2048 + AES-256"
    payloads = load_ehr_payloads(limit=50)

    enc_times = []
    plaintext_sizes = []

    print("Starting encryption benchmark...")

    # Encryption benchmark
    for p in payloads:
        plaintext = json.dumps(p, ensure_ascii=False).encode("utf-8")
        plaintext_sizes.append(len(plaintext))

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

    print("Encryption benchmark completed.")

    # Decryption benchmark (for first patient)
    test_pid = payloads[0]["patient_id"]

    print("Starting decryption benchmark...")

    t0 = time.perf_counter()
    records = fetch_and_decrypt_records("doctor1", "Doctor", test_pid)
    t1 = time.perf_counter()

    dec_time = (t1 - t0) * 1000.0

    print("Decryption benchmark completed.")

    print("\n=== Benchmark Results (RSA-2048 + AES-256) ===")
    print(f"Records encrypted: {len(payloads)}")
    print(f"Mean encryption time (ms): {stats.mean(enc_times):.3f}")
    print(f"Std encryption time (ms): {stats.pstdev(enc_times):.3f}")
    print(f"Decryption time (ms): {dec_time:.3f}")
    print(f"Mean plaintext size (bytes): {stats.mean(plaintext_sizes):.1f}")
    print(f"Max plaintext size (bytes): {max(plaintext_sizes)}")


if __name__ == "__main__":
    main()