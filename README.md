# Healthify Backend Engine ⚡

A secure, high-performance, and localized REST API engineered using FastAPI and PostgreSQL. Built as a robust digital healthcare backend, this system is architected to eliminate administrative gaps and streamline doctor-patient workflows through rigorous relational data tracking, cryptographic security, and state-driven transaction workflows.

---

## 🛠️ Core Engineering Highlights

* **Relational Database Integrity:** Engineered a strict 4-table relational database schema mapping relationships seamlessly across Users, Doctor Profiles, Appointments, and Clinical Medical Records via SQLAlchemy ORM.
* **Enterprise-Grade Security:** Enforced robust data privacy protocols utilizing cryptographic password hashing with **Passlib (Bcrypt)** and stateless session management powered by **JSON Web Tokens (JWT)**.
* **State-Driven Transactions:** Built explicit state tracking for appointment scheduling workflows, integrating an operational payment verification sequence (`is_paid` boolean state) that must validate successfully before a slot changes from pending to confirmed.
* **Decoupled Clinical Workflows:** Designed isolated medical report management mechanics, allowing practitioners to securely commit text diagnostics bound permanently to a persistent patient record.

---

## 💻 Tech Stack & Rationale

* **Framework:** **FastAPI** (Python) – Selected for asynchronous high performance, rapid development speeds, and native OpenAPI (Swagger) automated documentation generation.
* **Database:** **PostgreSQL** – Chosen to guarantee strict data integrity, complex transactional handling, and enterprise-scale indexing.
* **ORM:** **SQLAlchemy** – Utilized to translate application-layer logic cleanly into highly optimized SQL queries.
* **Security Layer:** **JWT (Python-Jose)** & **Bcrypt (Passlib)** – Integrated to satisfy strict platform authentication and security mandates.

---

## 📂 Project Architecture

```text
HEALTHIFY_BACKEND/
├── main.py          # FastAPI application initialization, security layers, and API routing
├── models.py        # SQLAlchemy database schemas, relational definitions, and data constraints
├── database.py      # PostgreSQL engine configuration and session allocation
├── .gitignore       # Strict version control filters (skips virtual environments & caches)
└── requirements.txt # Explicit production library dependencies

```

---

## 🚀 Quick Start Guide

Follow these steps to spin up the production backend engine locally:

### 1. Clone the Repository

```bash
git clone [https://github.com/AbdulRehman448/healthify-backend.git](https://github.com/AbdulRehman448/healthify-backend.git)
cd HEALTHIFY_BACKEND

```

### 2. Configure Your Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the environment (Windows)
.\venv\Scripts\activate.ps1

```

### 3. Install Production Dependencies

```bash
pip install -r requirements.txt

```

### 4. Initialize and Run the Server

Ensure your local PostgreSQL instance is running via pgAdmin, then execute:

```bash
uvicorn main:app --reload

```

Once initialized, navigate to **`http://127.0.0.1:8000/docs`** in your web browser to access the interactive Swagger API documentation.

---

## 👨‍💻 Developer

**Abdul Rehman Ali**

* **Email:** [abdulrehman.tp.786@gmail.com]()
* **LinkedIn:** [Abdul Rehman Ali](https://www.linkedin.com/in/abdul-rehman-ali/)

