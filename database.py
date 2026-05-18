from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. The Connection String
# Replace 'YOUR_PASSWORD' with the one you set during PostgreSQL installation
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:haq24.@localhost:5432/healthify_db"

# 2. Create the Engine (The Bridge)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. Create a Session (The Person who talks to the database)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. The Base (The Blueprint for your tables)
Base = declarative_base()