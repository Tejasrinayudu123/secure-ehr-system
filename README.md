# Secure Electronic Health Record (EHR) System with Hybrid Encryption

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Encryption](https://img.shields.io/badge/Encryption-AES256%20%2B%20RSA2048-green)
![Dataset](https://img.shields.io/badge/Dataset-MIMIC--IV-orange)
![Status](https://img.shields.io/badge/Project-Research%20Prototype-purple)

---

## Project Overview

Healthcare systems store highly sensitive patient data including medical history, diagnoses, and treatment information. Protecting this data is critical to ensure **privacy, confidentiality, and regulatory compliance**.

This project implements a **Secure Electronic Health Record (EHR) System** using a **Hybrid Encryption Architecture**.

The system uses:

- **AES-256-GCM** for encrypting medical records
- **RSA-2048** for secure encryption key management

Patient records are derived from the **MIMIC-IV clinical dataset**, encrypted, and stored securely in a database with **Role-Based Access Control (RBAC)**.

---

# Key Features

- Hybrid encryption (**AES-256 + RSA-2048**)
- Secure encrypted EHR database
- Role-Based Access Control (RBAC)
- Encryption benchmarking
- Storage overhead analysis
- Performance graph generation
- Architecture ready for **Post-Quantum Cryptography**

---

# System Architecture

The system follows a **secure layered architecture**.

### Frontend Layer *(Future Work)*

- Doctor Portal
- Patient Portal
- Admin Dashboard

### Backend Services

- Encryption services
- Decryption services
- Authentication
- RBAC verification

### Security Layer

- AES-256 encryption
- RSA-2048 key wrapping
- Secure authentication validation

### Database Layer

- Encrypted patient records
- User and role data
- Audit logs

---

# Technologies Used

| Technology | Purpose |
|--------|--------|
| Python 3.11 | Core implementation |
| SQLite | Secure encrypted database |
| AES-256-GCM | Data encryption |
| RSA-2048 | Secure key wrapping |
| Pandas | Dataset processing |
| Matplotlib | Performance visualization |
| MIMIC-IV | Healthcare dataset |

---

# Dataset

This project uses the **MIMIC-IV Clinical Database Demo Dataset**.

Dataset contents include:

- Patient demographics
- Hospital admissions
- Diagnosis codes
- Clinical visit information

Dataset Source:

https://physionet.org/content/mimic-iv-demo/

Example patient record:

```json
{
  "patient_id": "10014354",
  "admission_id": "29780751",
  "admission_type": "OBSERVATION ADMIT",
  "demographics": {
    "gender": "M",
    "age": 60
  },
  "diagnoses": [
    {"icd_code": "I10"},
    {"icd_code": "E039"}
  ]
}
```

---

# Project Structure

```
DBMS/
│
├── data/
│   └── mimiciv_demo/
│
├── src/
│   ├── api.py
│   ├── crypto_aes.py
│   ├── crypto_rsa.py
│   ├── db.py
│   └── mimic_loader.py
│
├── import_mimic.py
├── check_decrypt.py
├── benchmark_crypto.py
├── measure_storage_overhead.py
│
├── encryption_time_distribution.png
├── ciphertext_size_distribution.png
│
└── README.md
```

---

# Installation

Clone repository:

```
git clone https://github.com/YOUR_USERNAME/secure-ehr-system.git
cd secure-ehr-system
```

Create virtual environment:

```
python -m venv .venv
```

Activate environment (Windows):

```
.\.venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# Running the Project

### Import and Encrypt Dataset

```
python import_mimic.py
```

This script:

- Loads patient records
- Encrypts them using AES-256
- Wraps encryption keys using RSA-2048
- Stores encrypted records in the database

---

### Test Decryption

```
python check_decrypt.py
```

Verifies encrypted records can be securely decrypted.

---

### Run Encryption Benchmark

```
python benchmark_crypto.py
```

Measures:

- Encryption time
- Decryption time
- Plaintext size distribution

---

### Measure Storage Overhead

```
python measure_storage_overhead.py
```

Measures:

- Ciphertext size
- AES nonce size
- RSA wrapped key size
- Total storage overhead

---

# Benchmark Results

| Metric | Value |
|------|------|
| Encryption Algorithm | AES-256-GCM |
| Key Wrapping Algorithm | RSA-2048 |
| Mean Encryption Time | ~27 ms |
| Mean Decryption Time | ~15 ms |
| Average Ciphertext Size | ~869 bytes |
| Storage Overhead per Record | ~1137 bytes |

---

# Performance Graphs

### Encryption Time Distribution

![Encryption Time](encryption_time_distribution.png)

### Ciphertext Size Distribution

![Ciphertext Size](ciphertext_size_distribution.png)

---

# Security Features

The system ensures healthcare data security through:

- AES-256 encryption for patient records
- RSA-2048 secure key wrapping
- RBAC controlled data access
- Encrypted database storage

The architecture is designed to support **future Post-Quantum Cryptography algorithms such as CRYSTALS-Kyber**.

---

# Future Work

Future improvements may include:

- Full healthcare dashboard frontend
- Cloud-based EHR system
- Post-Quantum Cryptography integration
- Secure healthcare analytics
- Blockchain-based audit logging

---

# Author

**Tejasri Nayudu**  
Master’s in Computer Science

---

# License

This project is developed for academic and research purposes.