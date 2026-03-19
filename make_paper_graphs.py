import matplotlib.pyplot as plt
from pathlib import Path

OUTPUT_DIR = Path("paper_figures")
OUTPUT_DIR.mkdir(exist_ok=True)

# -----------------------------
# Graph 1: Your measured runtime
# -----------------------------
def plot_runtime_comparison():
    labels = ["Encryption", "Decryption"]
    values = [27.611, 15.255]  # your measured ms

    plt.figure(figsize=(6.5, 4.2))
    plt.bar(labels, values)
    plt.title("Measured Runtime for RSA-2048 + AES-256")
    plt.xlabel("Operation")
    plt.ylabel("Time (ms)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "fig_runtime_comparison.png", dpi=300)
    plt.close()


# ------------------------------------------------------
# Graph 2: Standards-based size comparison (AES/RSA/PQC)
# ------------------------------------------------------
def plot_crypto_size_comparison():
    labels = [
        "AES-256 Key",
        "RSA-2048\nWrapped Key",
        "ML-KEM-768\nCiphertext",
        "ML-KEM-768\nEncap Key",
        "ML-DSA-65\nSignature",
    ]
    values = [
        32,    # AES-256 key = 32 bytes
        256,   # RSA-2048 wrapped AES key = 256 bytes
        1088,  # ML-KEM-768 ciphertext
        1184,  # ML-KEM-768 encapsulation key
        3309,  # ML-DSA-65 signature
    ]

    plt.figure(figsize=(8.2, 4.6))
    plt.bar(labels, values)
    plt.title("Standards-Based Size Comparison: AES, RSA, and PQC Artifacts")
    plt.xlabel("Cryptographic Artifact")
    plt.ylabel("Size (bytes)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "fig_crypto_size_comparison.png", dpi=300)
    plt.close()


# -------------------------------------------------
# Graph 3: Your measured storage composition
# -------------------------------------------------
def plot_storage_composition():
    labels = ["Ciphertext", "Nonce", "Wrapped Key"]
    values = [869.5, 12, 256]  # your measured averages

    plt.figure(figsize=(6.8, 4.2))
    plt.bar(labels, values)
    plt.title("Measured Storage Composition per Encrypted Record")
    plt.xlabel("Stored Component")
    plt.ylabel("Average Size (bytes)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "fig_storage_composition.png", dpi=300)
    plt.close()


def main():
    plot_runtime_comparison()
    plot_crypto_size_comparison()
    plot_storage_composition()
    print("Saved figures in:", OUTPUT_DIR.resolve())


if __name__ == "__main__":
    main()