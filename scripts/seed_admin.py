"""
Запустите этот скрипт из папки backend:
python -m scripts.seed_admin
"""
import os
import sys
from dotenv import load_dotenv
from getpass import getpass

# добавить корень проекта в sys.path (чтобы импорт app работал)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# загрузка .env из папки backend
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

EMAIL = os.getenv("ADMIN_EMAIL") or input("Admin email: ").strip()
PASSWORD = os.getenv("ADMIN_PASS") or getpass("Admin password: ")

# импортируем внутренние модули
from app.database import SessionLocal, engine, Base
from app import crud, schemas, models

# создать таблицы (если нужно)
Base.metadata.create_all(bind=engine)

def main():
    db = SessionLocal()
    try:
        existing = crud.get_user_by_email(db, EMAIL)
        if existing:
            print("User exists:", existing.email)
        else:
            user_in = schemas.UserCreate(email=EMAIL, password=PASSWORD, full_name="Super Admin", role="SUPERADMIN")
            admin = crud.create_user(db, user_in)
            print("Created SUPERADMIN:", admin.email)
    finally:
        db.close()

if __name__ == "__main__":
    main()