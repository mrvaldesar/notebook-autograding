from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.models.audit import AuditActionEnum

class AuditLogBase(BaseModel):
    action: AuditActionEnum
    details: Optional[str] = None

class AuditLogCreate(AuditLogBase):
    evaluation_id: int
    user_id: Optional[int] = None

class AuditLogInDBBase(AuditLogBase):
    id: int
    evaluation_id: int
    user_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class AuditLog(AuditLogInDBBase):
    pass
