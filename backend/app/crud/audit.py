from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.audit import AuditLog, AuditActionEnum
from app.schemas.audit import AuditLogCreate

class CRUDAuditLog(CRUDBase[AuditLog, AuditLogCreate, AuditLogCreate]):
    def log_action(
        self, db: Session, *, evaluation_id: int, action: AuditActionEnum, user_id: int = None, details: str = None
    ) -> AuditLog:
        obj_in = AuditLogCreate(
            evaluation_id=evaluation_id,
            action=action,
            user_id=user_id,
            details=details
        )
        return self.create(db=db, obj_in=obj_in)

audit_log = CRUDAuditLog(AuditLog)
