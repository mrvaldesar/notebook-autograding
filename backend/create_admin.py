import os
import getpass
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User, RoleEnum

def create_admin_user():
    print("🎓 AI Autograder Platform - Setup Admin User")

    email = input("Enter admin email (e.g., admin@autograder.com): ").strip()
    if not email:
        print("Email cannot be empty.")
        return

    full_name = input("Enter full name: ").strip()

    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Confirm password: ")

    if password != confirm_password:
        print("Passwords do not match!")
        return

    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            print(f"User with email {email} already exists!")
            return

        admin_user = User(
            email=email,
            full_name=full_name,
            hashed_password=get_password_hash(password),
            role=RoleEnum.PROFESSOR,
            is_active=True
        )

        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print(f"✅ Successfully created admin/professor user: {email}")
        print("You can now log in to the frontend!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error creating user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
