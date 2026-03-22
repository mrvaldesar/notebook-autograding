from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

class AuditActionEnum(str, enum.Enum):
    EVALUATION_STARTED = "evaluation_started"
    EVALUATION_COMPLETED = "evaluation_completed"
    EVALUATION_FAILED = "evaluation_failed"
    SCORE_OVERRIDE = "score_override"

class AuditLog(Base):
    id = Column(Integer, primary_key=True, index=True)
    evaluation_id = Column(Integer, ForeignKey("evaluation.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True) # ID of user making change (e.g. professor overriding)
    action = Column(Enum(AuditActionEnum), nullable=False)
    details = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    evaluation = relationship("Evaluation")
    user = relationship("User")
