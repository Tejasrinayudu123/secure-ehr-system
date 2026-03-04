import sqlite3
import statistics as stats
from pathlib import Path

DB_PATH = Path("ehr_demo.sqlite3")  # change if your db file name is different

def main():
    if not DB_PATH.exists():
        print(f"❌ DB not found: {DB_PATH.resolve()}")
        return

    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        "SELECT scheme, length(ciphertext) AS ct_len, length(nonce) AS nonce_len, length(wrapped_key) AS wk_len "
        "FROM medical_records ORDER BY created_at DESC LIMIT 200"
    ).fetchall()
    con.close()

    if not rows:
        print("❌ No records found in medical_records")
        return

    ct = [r["ct_len"] for r in rows]
    nonce = [r["nonce_len"] for r in rows]
    wk = [r["wk_len"] for r in rows]
    scheme = rows[0]["scheme"]

    # AES-GCM nonce is usually 12 bytes; wrapped_key for RSA-2048 is usually 256 bytes
    print(f"Scheme: {scheme}")
    print(f"Records sampled: {len(rows)}\n")

    print("Ciphertext length (bytes)")
    print(f"  mean: {stats.mean(ct):.1f}")
    print(f"  min : {min(ct)}")
    print(f"  max : {max(ct)}\n")

    print("Nonce length (bytes)")
    print(f"  mean: {stats.mean(nonce):.1f}")
    print(f"  unique values: {sorted(set(nonce))}\n")

    print("Wrapped key length (bytes)")
    print(f"  mean: {stats.mean(wk):.1f}")
    print(f"  unique values: {sorted(set(wk))}\n")

    # Total storage per record (excluding other columns)
    total = [ct[i] + nonce[i] + wk[i] for i in range(len(rows))]
    print("Total crypto storage per record (ciphertext + nonce + wrapped_key)")
    print(f"  mean: {stats.mean(total):.1f} bytes")
    print(f"  min : {min(total)} bytes")
    print(f"  max : {max(total)} bytes")

if __name__ == "__main__":
    main()