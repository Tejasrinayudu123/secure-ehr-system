ROLE_DOCTOR = "Doctor"
ROLE_NURSE = "Nurse"
ROLE_PATIENT = "Patient"
ROLE_ADMIN = "Administrator"
ROLE_SECURITY = "Security Officer"

def can_view(role: str, user_id: str, patient_id: str) -> bool:
    if role in (ROLE_DOCTOR, ROLE_NURSE, ROLE_ADMIN, ROLE_SECURITY):
        return True
    if role == ROLE_PATIENT:
        return user_id == patient_id
    return False