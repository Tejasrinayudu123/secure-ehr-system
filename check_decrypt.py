import sqlite3
from pathlib import Path

from src.api import login, fetch_and_decrypt_records

DB_PATH = Path("ehr_demo.sqlite3")  # change only if your DB file name differs


def main():
    if not DB_PATH.exists():
        print(f"❌ Database not found: {DB_PATH.resolve()}")
        print("Run: python import_mimic.py")
        return

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM medical_records")
    total = cur.fetchone()[0]
    print("Total encrypted records in DB:", total)

    if total == 0:
        print("❌ No records found. Run: python import_mimic.py")
        con.close()
        return

    cur.execute(
        "SELECT patient_id, COUNT(*) as n FROM medical_records GROUP BY patient_id ORDER BY n DESC LIMIT 10"
    )
    top = cur.fetchall()
    con.close()

    print("\nTop patient_ids in DB:")
    for pid, n in top:
        print(f" - {pid} ({n} records)")

    patient_id = str(top[0][0])
    print("\nTesting decrypt for patient_id:", patient_id)

    login("doctor1", "Doctor")
    records = fetch_and_decrypt_records("doctor1", "Doctor", patient_id)

    print(f"\n✅ Decrypted {len(records)} record(s). First record:\n")
    print(records[0].decode("utf-8", errors="replace"))


if __name__ == "__main__":
    main()