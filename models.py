from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base

class User(Base):
    """Stores all platform users with encrypted passwords."""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String)  # 'Patient' or 'Doctor' [cite: 70, 71]

class DoctorProfile(Base):
    """Extensions for users with the 'Doctor' role."""
    __tablename__ = "doctor_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    specialty = Column(String)
    is_verified = Column(Boolean, default=False)  # For Admin verification [cite: 85]
    consultation_hours = Column(String)

class Appointment(Base):
    """Manages localized scheduling and payment status[cite: 75, 80]."""
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    doctor_id = Column(Integer, ForeignKey("doctor_profiles.id"))
    appointment_date = Column(String)
    status = Column(String, default="Pending")
    is_paid = Column(Boolean, default=False)  # Secure Payment requirement 

class MedicalReport(Base):
    """Handles doctor diagnoses and results."""
    __tablename__ = "medical_reports"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    doctor_id = Column(Integer, ForeignKey("doctor_profiles.id"))
    diagnosis_details = Column(String)
    report_url = Column(String, nullable=True)
    created_at = Column(String)