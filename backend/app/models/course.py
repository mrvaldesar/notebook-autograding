from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base
from datetime import datetime

class Course(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    professor_id = Column(Integer, ForeignKey("user.id"))

    professor = relationship("User", backref="courses")
    assignments = relationship("Assignment", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")

class Enrollment(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    enrolled_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="enrollments")
    course = relationship("Course", back_populates="enrollments")

class DockerEnvEnum(str, enum.Enum):
    BASIC = "basic"
    DEEP_LEARNING = "deep_learning"

class Assignment(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    due_date = Column(DateTime)
    docker_env = Column(Enum(DockerEnvEnum), default=DockerEnvEnum.BASIC)
    hidden_dataset_path = Column(String, nullable=True) # Path to the hidden test set

    course = relationship("Course", back_populates="assignments")
    rubric = relationship("Rubric", back_populates="assignment", uselist=False)

from sqlalchemy.dialects.postgresql import JSONB

class Rubric(Base):
    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignment.id"), nullable=False, unique=True)
    criteria = Column(JSONB, nullable=False) # e.g. [{"name": "tests", "weight": 40}, {"name": "ml_accuracy", "weight": 30, "metric": "accuracy", "threshold": 0.85}]

    assignment = relationship("Assignment", back_populates="rubric")
