import json
import time
import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt

from src.api import login, encrypt_and_store_record
from src.mimic_loader import load_ehr_payloads


DB_PATH = Path("ehr_demo.sqlite3")   # change only if your DB filename is different
SCHEME = "RSA-2048 + AES-256"


def plot_encryption_time_histogram(n_records: int = 50):
    login("doctor1", "Doctor")
    payloads = load_ehr_payloads(limit=n_records)

    enc_times_ms = []

    for p in payloads:
        plaintext = json.dumps(p, ensure_ascii=False).encode("utf-8")

        t0 = time.perf_counter()
        encrypt_and_store_record(
            user_id="doctor1",
            role="Doctor",
            patient_id=p["patient_id"],
            plaintext=plaintext,
            scheme=SCHEME,
        )
        t1 = time.perf_counter()
        enc_times_ms.append((t1 - t0) * 1000.0)

    plt.figure()
    plt.hist(enc_times_ms, bins=12)
    plt.title("Encryption Time Distribution (RSA-2048 + AES-256)")
    plt.xlabel("Encryption time per record (ms)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("fig_encryption_time_hist.png", dpi=300)
    plt.close()

    print("✅ Saved: fig_encryption_time_hist.png")


def plot_ciphertext_size_histogram(sample_n: int = 200):
    if not DB_PATH.exists():
        print(f"❌ DB not found: {DB_PATH.resolve()}")
        print("Run: python import_mimic.py (or python benchmark_crypto.py) first.")
        return

    con = sqlite3.connect(DB_PATH)
    rows = con.execute(
        "SELECT length(ciphertext) AS ct_len "
        "FROM medical_records "
        "WHERE scheme=? "
        "ORDER BY created_at DESC "
        "LIMIT ?",
        (SCHEME, sample_n),
    ).fetchall()
    con.close()

    if not rows:
        print("❌ No ciphertext rows found in DB.")
        return

    ct_lens = [r[0] for r in rows]

    plt.figure()
    plt.hist(ct_lens, bins=12)
    plt.title("Ciphertext Size Distribution (AES-GCM ciphertext bytes)")
    plt.xlabel("Ciphertext size (bytes)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("fig_ciphertext_size_hist.png", dpi=300)
    plt.close()

    print("✅ Saved: fig_ciphertext_size_hist.png")


def main():
    # 1) Encryption time graph (adds n_records new encrypted rows to your DB)
    plot_encryption_time_histogram(n_records=50)

    # 2) Ciphertext size graph (reads from DB)
    plot_ciphertext_size_histogram(sample_n=200)


if __name__ == "__main__":
    main()