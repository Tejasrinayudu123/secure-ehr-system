import pandas as pd
from pathlib import Path

HOSP = Path("data") / "mimiciv_demo" / "hosp"

def load_ehr_payloads(limit: int = 200):
    patients = pd.read_csv(HOSP / "patients.csv.gz", compression="gzip")
    admissions = pd.read_csv(HOSP / "admissions.csv.gz", compression="gzip")
    dx = pd.read_csv(HOSP / "diagnoses_icd.csv.gz", compression="gzip")

    patients = patients[["subject_id", "gender", "anchor_age"]]
    admissions = admissions[["subject_id", "hadm_id", "admittime", "dischtime", "admission_type"]]
    dx = dx[["subject_id", "hadm_id", "icd_code", "icd_version"]]

    ehr = admissions.merge(patients, on="subject_id", how="left").merge(dx, on=["subject_id", "hadm_id"], how="left")

    grouped = ehr.groupby(
        ["subject_id", "hadm_id", "admittime", "dischtime", "admission_type", "gender", "anchor_age"],
        dropna=False
    )

    payloads = []
    for key, g in grouped:
        subject_id, hadm_id, admittime, dischtime, admission_type, gender, anchor_age = key

        diagnoses = (
            g[["icd_code", "icd_version"]]
            .dropna()
            .drop_duplicates()
            .head(20)
            .to_dict("records")
        )

        payloads.append({
            "patient_id": str(subject_id),
            "admission_id": str(hadm_id),
            "admission_type": None if pd.isna(admission_type) else str(admission_type),
            "admittime": str(admittime),
            "dischtime": str(dischtime),
            "demographics": {
                "gender": None if pd.isna(gender) else str(gender),
                "anchor_age": None if pd.isna(anchor_age) else int(anchor_age),
            },
            "diagnoses": diagnoses,
            "ehr_note": "Derived from MIMIC-IV Demo (structured tables; no free-text notes)."
        })

        if len(payloads) >= limit:
            break

    return payloads