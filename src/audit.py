from datetime import datetime, timezone
from src.db import connect

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def log_event(user_id: str, role: str, action: str, patient_id: str | None = None, details: str | None = None) -> None:
    con = connect()
    try:
        with con:
            con.execute(
                "INSERT INTO audit_logs(user_id, role, action, patient_id, details, ts) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, role, action, patient_id, details, now_iso())
            )
    finally:
        con.close()