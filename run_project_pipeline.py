import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.resolve()


def run_step(script_name: str, description: str):
    print("\n" + "=" * 60)
    print(f"STEP: {description}")
    print("=" * 60)

    script_path = PROJECT_ROOT / script_name

    if not script_path.exists():
        print(f"❌ File not found: {script_path}")
        return False

    result = subprocess.run([sys.executable, str(script_path)], cwd=PROJECT_ROOT)

    if result.returncode != 0:
        print(f"❌ Step failed: {script_name}")
        return False

    print(f"✅ Step completed: {script_name}")
    return True


def main():
    print("\nStarting Secure EHR Project Pipeline...\n")

    steps = [
        ("import_mimic.py", "Import and encrypt dataset records"),
        ("check_decrypt.py", "Verify secure decryption"),
        ("benchmark_crypto.py", "Run encryption performance benchmark"),
        ("measure_storage_overhead.py", "Measure storage overhead"),
        ("view_audit_logs.py", "Display audit logs"),
        ("detect_intrusions.py", "Run intrusion detection"),
        ("backup_db.py", "Create database backup"),
        ("export_results.py", "Export results to CSV"),
        ("security_report.py", "Generate security report"),
    ]

    for script, description in steps:
        success = run_step(script, description)
        if not success:
            print("\n⚠️ Pipeline stopped due to error.")
            return

    print("\n" + "=" * 60)
    print("✅ FULL PROJECT PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print("\nOutputs generated may include:")
    print("- Encrypted medical records in SQLite database")
    print("- Audit logs")
    print("- Benchmark statistics")
    print("- Storage overhead analysis")
    print("- Database backup file")
    print("- CSV result exports")
    print("- Security report summary")


if __name__ == "__main__":
    main()