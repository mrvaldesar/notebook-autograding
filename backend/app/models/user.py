from sqlalchemy import Column, Integer, String, Boolean, Enum
import enum
from app.db.base_class import Base

class RoleEnum(str, enum.Enum):
    PROFESSOR = "professor"
    STUDENT = "student"

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    student_id = Column(String, index=True, nullable=True) # Carnet
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    role = Column(Enum(RoleEnum), nullable=False)
