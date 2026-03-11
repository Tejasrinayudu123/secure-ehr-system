import sqlite3
from pathlib import Path

DB_PATH = Path("ehr_demo.sqlite3")  # change only if your DB file name differs

def main():
    if not DB_PATH.exists():
        print(f"❌ Database not found: {DB_PATH.resolve()}")
        return

    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row

    rows = con.execute(
        """
        SELECT log_id, user_id, role, action, patient_id, details, ts
        FROM audit_logs
        ORDER BY ts DESC
        LIMIT 100
        """
    ).fetchall()

    con.close()

    if not rows:
        print("❌ No audit logs found.")
        return

    print("\n=== Audit Logs (Latest 100) ===\n")
    for row in rows:
        print(f"[{row['ts']}] "
              f"User={row['user_id']} | "
              f"Role={row['role']} | "
              f"Action={row['action']} | "
              f"Patient={row['patient_id']} | "
              f"Details={row['details']}")

if __name__ == "__main__":
    main()