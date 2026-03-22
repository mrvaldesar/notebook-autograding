from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from app.models.submission import EvaluationStatus

class EvaluationBase(BaseModel):
    status: Optional[EvaluationStatus] = EvaluationStatus.PENDING
    score: Optional[float] = None
    feedback: Optional[Dict[str, Any]] = None
    manual_override: Optional[bool] = False

class EvaluationCreate(EvaluationBase):
    notebook_version_id: int

class EvaluationUpdate(EvaluationBase):
    execution_logs: Optional[str] = None

class EvaluationInDBBase(EvaluationBase):
    id: int
    notebook_version_id: int
    execution_logs: Optional[str] = None

    class Config:
        from_attributes = True

class Evaluation(EvaluationInDBBase):
    pass

class NotebookVersionBase(BaseModel):
    version_number: int
    file_path: str

class NotebookVersionCreate(NotebookVersionBase):
    submission_id: int

class NotebookVersionInDBBase(NotebookVersionBase):
    id: int
    submission_id: int
    submitted_at: datetime
    evaluation: Optional[Evaluation] = None

    class Config:
        from_attributes = True

class NotebookVersion(NotebookVersionInDBBase):
    pass

class SubmissionBase(BaseModel):
    pass

class SubmissionCreate(SubmissionBase):
    assignment_id: int
    student_id: int

class SubmissionInDBBase(SubmissionBase):
    id: int
    assignment_id: int
    student_id: int
    versions: List[NotebookVersion] = []

    class Config:
        from_attributes = True

class Submission(SubmissionInDBBase):
    pass
