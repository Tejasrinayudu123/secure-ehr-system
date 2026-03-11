import sqlite3
from pathlib import Path
from collections import Counter
import statistics as stats

DB_PATH = Path("ehr_demo.sqlite3")
OUTPUT_DIR = Path("results")


def main():
    if not DB_PATH.exists():
        print(f"❌ Database not found: {DB_PATH.resolve()}")
        return

    OUTPUT_DIR.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # -----------------------------
    # 1. Medical record statistics
    # -----------------------------
    medical_rows = conn.execute("""
        SELECT patient_id,
               LENGTH(ciphertext) AS ciphertext_size,
               LENGTH(nonce) AS nonce_size,
               LENGTH(wrapped_key) AS wrapped_key_size
        FROM medical_records
    """).fetchall()

    # -----------------------------
    # 2. Audit log statistics
    # -----------------------------
    audit_rows = conn.execute("""
        SELECT user_id, role, action, patient_id, details, ts
        FROM audit_logs
        ORDER BY ts DESC
    """).fetchall()

    conn.close()

    if not medical_rows:
        print("❌ No encrypted medical records found.")
        return

    # Medical stats
    ciphertext_sizes = [row["ciphertext_size"] for row in medical_rows]
    nonce_sizes = [row["nonce_size"] for row in medical_rows]
    wrapped_key_sizes = [row["wrapped_key_size"] for row in medical_rows]

    total_crypto_sizes = [
        row["ciphertext_size"] + row["nonce_size"] + row["wrapped_key_size"]
        for row in medical_rows
    ]

    # Audit stats
    action_counter = Counter()
    user_counter = Counter()
    suspicious_counter = Counter()

    for row in audit_rows:
        action = row["action"] or "UNKNOWN"
        user = row["user_id"] or "UNKNOWN"

        action_counter[action] += 1
        user_counter[user] += 1

        if "DENY" in action.upper() or "denied" in (row["details"] or "").lower():
            suspicious_counter[user] += 1

    # -----------------------------
    # Print report
    # -----------------------------
    print("\n==============================")
    print("   SECURITY REPORT SUMMARY")
    print("==============================\n")

    print("1. Medical Record Security Statistics")
    print("-------------------------------------")
    print(f"Total encrypted records          : {len(medical_rows)}")
    print(f"Average ciphertext size          : {stats.mean(ciphertext_sizes):.2f} bytes")
    print(f"Minimum ciphertext size          : {min(ciphertext_sizes)} bytes")
    print(f"Maximum ciphertext size          : {max(ciphertext_sizes)} bytes")
    print(f"Average nonce size               : {stats.mean(nonce_sizes):.2f} bytes")
    print(f"Average wrapped key size         : {stats.mean(wrapped_key_sizes):.2f} bytes")
    print(f"Average total crypto storage     : {stats.mean(total_crypto_sizes):.2f} bytes")

    print("\n2. Audit Log Summary")
    print("--------------------")
    print(f"Total audit events               : {len(audit_rows)}")
    print("Action distribution:")
    for action, count in action_counter.items():
        print(f"  - {action}: {count}")

    print("\n3. Most Active Users")
    print("--------------------")
    for user, count in user_counter.most_common(5):
        print(f"  - {user}: {count} actions")

    print("\n4. Suspicious / Denied Activity")
    print("-------------------------------")
    if suspicious_counter:
        for user, count in suspicious_counter.items():
            print(f"  ⚠️ {user}: {count} denied/suspicious events")
    else:
        print("  ✅ No suspicious denied activity detected.")

    print("\n==============================")
    print(" End of Security Report")
    print("==============================\n")


if __name__ == "__main__":
    main()