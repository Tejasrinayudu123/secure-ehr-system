from pathlib import Path
from datetime import datetime
import shutil

# Change only if your database file name is different
DB_PATH = Path("ehr_demo.sqlite3")
BACKUP_DIR = Path("backups")


def main():
    if not DB_PATH.exists():
        print(f"❌ Database not found: {DB_PATH.resolve()}")
        return

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"ehr_demo_backup_{timestamp}.sqlite3"

    shutil.copy2(DB_PATH, backup_file)

    print("✅ Database backup created successfully.")
    print(f"Source : {DB_PATH.resolve()}")
    print(f"Backup : {backup_file.resolve()}")


if __name__ == "__main__":
    main()