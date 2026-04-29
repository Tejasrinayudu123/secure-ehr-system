import json
import time
import statistics as stats
import hashlib
from pathlib import Path

from src.crypto_aes import aes_encrypt, aes_decrypt
from src.mimic_loader import load_ehr_payloads


# Standards-based artifact sizes in bytes
KYBER_768_PUBLIC_KEY = 1184
KYBER_768_CIPHERTEXT = 1088
DILITHIUM_SIGNATURE = 3309
AES_256_KEY = 32


def derive_aes_key_from_simulated_kyber_secret(patient_id: str) -> bytes:
    """
    Simulates Kyber shared-secret derivation.
    This is NOT real Kyber encryption.
    It is a technical simulation for migration analysis.
    """
    seed = f"simulated-kyber-shared-secret-{patient_id}".encode("utf-8")
    return hashlib.sha256(seed).digest()


def simulate_dilithium_signature(ciphertext: bytes) -> bytes:
    """
    Simulates Dilithium signature storage overhead.
    This is NOT real Dilithium signing.
    """
    digest = hashlib.sha256(ciphertext).digest()
    return digest + bytes(DILITHIUM_SIGNATURE - len(digest))


def main():
    payloads = load_ehr_payloads(limit=50)

    encryption_times = []
    total_storage_sizes = []

    for p in payloads:
        plaintext = json.dumps(p, ensure_ascii=False).encode("utf-8")

        aes_key = derive_aes_key_from_simulated_kyber_secret(p["patient_id"])

        start = time.perf_counter()
        blob = aes_encrypt(aes_key, plaintext)
        end = time.perf_counter()

        signature = simulate_dilithium_signature(blob.ciphertext)

        total_storage = (
            len(blob.ciphertext)
            + len(blob.nonce)
            + KYBER_768_CIPHERTEXT
            + len(signature)
        )

        encryption_times.append((end - start) * 1000)
        total_storage_sizes.append(total_storage)

        # Verify decrypt still works
        recovered = aes_decrypt(aes_key, blob)
        assert recovered == plaintext

    print("\n=== PQC Migration Simulation Results ===")
    print("Mode: AES-256 + Simulated Kyber-768 + Simulated Dilithium")
    print(f"Records tested: {len(payloads)}")
    print(f"Mean AES encryption time (ms): {stats.mean(encryption_times):.3f}")
    print(f"Std AES encryption time (ms): {stats.pstdev(encryption_times):.3f}")
    print(f"Mean estimated PQC storage per record (bytes): {stats.mean(total_storage_sizes):.1f}")
    print(f"Min estimated storage (bytes): {min(total_storage_sizes)}")
    print(f"Max estimated storage (bytes): {max(total_storage_sizes)}")
    print("\nNote: Kyber and Dilithium are simulated using NIST artifact sizes.")
    print("This script is for migration overhead analysis, not production cryptography.")


if __name__ == "__main__":
    main()