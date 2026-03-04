import pandas as pd
from pathlib import Path

BASE = Path("data") / "mimiciv_demo" / "hosp"

patients_path = BASE / "patients.csv.gz"
admissions_path = BASE / "admissions.csv.gz"
diagnoses_path = BASE / "diagnoses_icd.csv.gz"

print("Checking dataset paths...")

print("Patients:", patients_path.exists())
print("Admissions:", admissions_path.exists())
print("Diagnoses:", diagnoses_path.exists())

patients = pd.read_csv(patients_path, compression="gzip")
admissions = pd.read_csv(admissions_path, compression="gzip")
diagnoses = pd.read_csv(diagnoses_path, compression="gzip")

print("\n✅ Dataset Loaded Successfully!")

print("\nPatients Shape:", patients.shape)
print("Admissions Shape:", admissions.shape)
print("Diagnoses Shape:", diagnoses.shape)

print("\nSample Patients Data:")
print(patients.head())