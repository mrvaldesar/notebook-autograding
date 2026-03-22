from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

class EvaluationStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class Submission(Base):
    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignment.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    assignment = relationship("Assignment")
    student = relationship("User")
    versions = relationship("NotebookVersion", back_populates="submission", order_by="NotebookVersion.version_number")

class NotebookVersion(Base):
    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submission.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    file_path = Column(String, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    submission = relationship("Submission", back_populates="versions")
    evaluation = relationship("Evaluation", back_populates="notebook_version", uselist=False)

class Evaluation(Base):
    id = Column(Integer, primary_key=True, index=True)
    notebook_version_id = Column(Integer, ForeignKey("notebookversion.id"), nullable=False, unique=True)
    status = Column(Enum(EvaluationStatus), default=EvaluationStatus.PENDING)
    score = Column(Float, nullable=True) # 0-100
    feedback = Column(JSONB, nullable=True) # Structured feedback
    execution_logs = Column(String, nullable=True)
    manual_override = Column(Boolean, default=False)

    notebook_version = relationship("NotebookVersion", back_populates="evaluation")
