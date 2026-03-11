from src.api import login, fetch_and_decrypt_records


def test_doctor_access(patient_id: str):
    print("\n=== Test 1: Doctor Access ===")
    try:
        login("doctor1", "Doctor")
        records = fetch_and_decrypt_records("doctor1", "Doctor", patient_id)
        print(f"✅ Doctor access allowed. Records decrypted: {len(records)}")
    except Exception as e:
        print(f"❌ Doctor access failed: {e}")


def test_patient_own_access(patient_id: str):
    print("\n=== Test 2: Patient Own Record Access ===")
    try:
        login(patient_id, "Patient")
        records = fetch_and_decrypt_records(patient_id, "Patient", patient_id)
        print(f"✅ Patient own-record access allowed. Records decrypted: {len(records)}")
    except Exception as e:
        print(f"❌ Patient own-record access failed: {e}")


def test_patient_other_access(patient_id: str):
    print("\n=== Test 3: Patient Unauthorized Access ===")
    try:
        login("patient_test_user", "Patient")
        records = fetch_and_decrypt_records("patient_test_user", "Patient", patient_id)
        print(f"❌ Unauthorized access incorrectly allowed. Records decrypted: {len(records)}")
    except Exception as e:
        print(f"✅ Unauthorized access correctly denied: {e}")


def test_admin_access(patient_id: str):
    print("\n=== Test 4: Administrator Access ===")
    try:
        login("admin1", "Administrator")
        records = fetch_and_decrypt_records("admin1", "Administrator", patient_id)
        print(f"✅ Administrator access allowed. Records decrypted: {len(records)}")
    except Exception as e:
        print(f"❌ Administrator access failed: {e}")


def main():
    # Use a patient_id that exists in your DB
    test_patient_id = "10014354"

    test_doctor_access(test_patient_id)
    test_patient_own_access(test_patient_id)
    test_patient_other_access(test_patient_id)
    test_admin_access(test_patient_id)

    print("\nRBAC testing completed.")


if __name__ == "__main__":
    main()