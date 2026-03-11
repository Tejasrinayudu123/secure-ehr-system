import sqlite3
import csv
from pathlib import Path

DB_PATH = Path("ehr_demo.sqlite3")
OUTPUT_DIR = Path("results")


def export_encryption_data():
    if not DB_PATH.exists():
        print("❌ Database not found.")
        return

    OUTPUT_DIR.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    rows = cursor.execute("""
        SELECT patient_id,
               LENGTH(ciphertext),
               LENGTH(nonce),
               LENGTH(wrapped_key)
        FROM medical_records
    """).fetchall()

    output_file = OUTPUT_DIR / "encryption_storage_results.csv"

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "patient_id",
            "ciphertext_size",
            "nonce_size",
            "wrapped_key_size"
        ])

        for row in rows:
            writer.writerow(row)

    conn.close()

    print(f"✅ Results exported successfully")
    print(f"📁 File saved at: {output_file.resolve()}")


if __name__ == "__main__":
    export_encryption_data()