from src.crypto_pqc import mldsa_keygen, mldsa_sign, mldsa_verify

def main():
    kp = mldsa_keygen()
    message = b"test message for ML-DSA-65"
    signature = mldsa_sign(kp.sig, message)
    ok = mldsa_verify(kp.public_key, message, signature)
    print("Signature valid:", ok)

if __name__ == "__main__":
    main()