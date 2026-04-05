import matplotlib.pyplot as plt

# Standards-based sizes in bytes
labels = [
    "AES-256\nKey",
    "RSA-2048\nWrapped Key",
    "ML-KEM-768\nCiphertext",
    "ML-KEM-768\nEncap Key",
    "ML-DSA-65\nSignature"
]

values = [
    32,    # AES-256 key
    256,   # RSA-2048 wrapped AES key
    1088,  # ML-KEM-768 ciphertext
    1184,  # ML-KEM-768 encapsulation key
    3309   # ML-DSA-65 signature
]

# Two-color grouped style
colors = [
    "#2E8B57",  # green for classical
    "#2E8B57",
    "#C0504D",  # red for PQC
    "#C0504D",
    "#C0504D"
]

plt.figure(figsize=(8, 4.8))
bars = plt.bar(labels, values, color=colors)

for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 40,
        f"{int(height)}",
        ha="center",
        va="bottom",
        fontsize=9
    )

plt.title("Classical vs Post-Quantum Cryptographic Artifact Sizes")
plt.xlabel("Cryptographic Component")
plt.ylabel("Size (bytes)")
plt.tight_layout()

plt.savefig("pqc_comparison_graph.png", dpi=300)
plt.show()