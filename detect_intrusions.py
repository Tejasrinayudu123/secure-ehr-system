import sqlite3
from pathlib import Path
from collections import Counter

DB_PATH = Path("ehr_demo.sqlite3")  # change only if your DB file name differs

# Simple thresholds for suspicious behavior
MAX_READS_PER_USER = 10
MAX_DENIED_EVENTS_PER_USER = 3

def main():
    if not DB_PATH.exists():
        print(f"❌ Database not found: {DB_PATH.resolve()}")
        return

    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row

    rows = con.execute(
        """
        SELECT user_id, role, action, patient_id, details, ts
        FROM audit_logs
        ORDER BY ts DESC
        LIMIT 500
        """
    ).fetchall()

    con.close()

    if not rows:
        print("❌ No audit logs found.")
        return

    read_counter = Counter()
    deny_counter = Counter()

    for row in rows:
        action = row["action"] or ""
        user_id = row["user_id"] or "UNKNOWN"

        if action in ("READ_RECORD", "DECRYPT_RECORD"):
            read_counter[user_id] += 1

        if "DENY" in action.upper() or "denied" in (row["details"] or "").lower():
            deny_counter[user_id] += 1

    print("\n=== Intrusion Detection Report ===\n")

    suspicious_found = False

    print("Users with unusually high read activity:")
    for user, count in read_counter.items():
        if count > MAX_READS_PER_USER:
            suspicious_found = True
            print(f"⚠️  Suspicious read volume: User={user}, Reads={count}")

    print("\nUsers with repeated denied access attempts:")
    for user, count in deny_counter.items():
        if count > MAX_DENIED_EVENTS_PER_USER:
            suspicious_found = True
            print(f"⚠️  Possible intrusion attempt: User={user}, DeniedEvents={count}")

    if not suspicious_found:
        print("✅ No obvious suspicious activity detected based on current thresholds.")

if __name__ == "__main__":
    main()