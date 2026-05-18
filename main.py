from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import models
from database import engine, SessionLocal

# --- SECURITY SETUP  ---
SECRET_KEY = "healthify_production_secret_kharian_2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 1. Initialize the FastAPI instance
app = FastAPI(
    title="Healthify API", 
    description="Localized Healthcare Solution for Kharian"
)

# 2. Add CORS Middleware here so your React Frontend (Port 5173) is authorized
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, PUT, OPTIONS
    allow_headers=["*"],  # Allows Authorization headers
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- AUTHENTICATION & USER MANAGEMENT  ---

@app.post("/register", tags=["Authentication"], status_code=status.HTTP_201_CREATED)
def register(name: str, email: str, password: str, role: str, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed = pwd_context.hash(password)
    new_user = models.User(full_name=name, email=email, password_hash=hashed, role=role)
    db.add(new_user)
    db.commit()
    return {"message": f"Account created for {name}"}

@app.post("/login", tags=["Authentication"])
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not pwd_context.verify(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer", "user_id": user.id}

# --- DOCTOR SERVICES & DISCOVERY ---

@app.post("/doctor/profile", tags=["Doctors"])
def complete_profile(user_id: int, specialty: str, hours: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user or user.role != "Doctor":
        raise HTTPException(status_code=400, detail="User is not registered as a Doctor")
    
    new_profile = models.DoctorProfile(user_id=user_id, specialty=specialty, consultation_hours=hours)
    db.add(new_profile)
    db.commit()
    return {"message": "Doctor profile initialized "}

@app.get("/doctors/search", tags=["Discovery"])
def search_specialists(specialty: str, db: Session = Depends(get_db)):
    return db.query(models.DoctorProfile).filter(models.DoctorProfile.specialty.ilike(f"%{specialty}%")).all()

# --- APPOINTMENTS & PAYMENTS ---

@app.post("/book", tags=["Appointments"])
def book_appointment(patient_id: int, doctor_id: int, date: str, db: Session = Depends(get_db)):
    new_booking = models.Appointment(patient_id=patient_id, doctor_id=doctor_id, appointment_date=date)
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return {"message": "Booking received. Please complete payment.", "booking_id": new_booking.id}

@app.put("/appointment/confirm-payment/{booking_id}", tags=["Payments"])
def confirm_payment(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(models.Appointment).filter(models.Appointment.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking.is_paid = True
    booking.status = "Confirmed"
    db.commit()
    return {"message": "Payment verified and appointment confirmed "}

# --- CLINICAL REPORTS  ---

@app.post("/doctor/upload-report", tags=["Reports"])
def upload_report(patient_id: int, doctor_id: int, diagnosis: str, date: str, db: Session = Depends(get_db)):
    new_report = models.MedicalReport(patient_id=patient_id, doctor_id=doctor_id, diagnosis_details=diagnosis, created_at=date)
    db.add(new_report)
    db.commit()
    return {"message": "Diagnosis report uploaded successfully"}

# --- ADMIN OVERSIGHT ---

@app.put("/admin/verify-doctor/{profile_id}", tags=["Admin"])
def verify_doctor(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(models.DoctorProfile).filter(models.DoctorProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Doctor profile not found")
    
    profile.is_verified = True
    db.commit()
    return {"message": f"Specialist verified by Admin"}