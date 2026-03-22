from typing import Optional, List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.submission import Submission, NotebookVersion, Evaluation, EvaluationStatus
from app.schemas.submission import SubmissionCreate, SubmissionBase, NotebookVersionCreate, NotebookVersionBase, EvaluationCreate, EvaluationUpdate

class CRUDSubmission(CRUDBase[Submission, SubmissionCreate, SubmissionBase]):
    def get_by_assignment_and_student(
        self, db: Session, *, assignment_id: int, student_id: int
    ) -> Optional[Submission]:
        return (
            db.query(self.model)
            .filter(Submission.assignment_id == assignment_id, Submission.student_id == student_id)
            .first()
        )

class CRUDNotebookVersion(CRUDBase[NotebookVersion, NotebookVersionCreate, NotebookVersionBase]):
    def get_multi_by_submission(
        self, db: Session, *, submission_id: int, skip: int = 0, limit: int = 100
    ) -> List[NotebookVersion]:
         return (
             db.query(self.model)
             .filter(NotebookVersion.submission_id == submission_id)
             .order_by(NotebookVersion.version_number.desc())
             .offset(skip)
             .limit(limit)
             .all()
         )

class CRUDEvaluation(CRUDBase[Evaluation, EvaluationCreate, EvaluationUpdate]):
    def get_by_notebook_version(
        self, db: Session, *, notebook_version_id: int
    ) -> Optional[Evaluation]:
        return (
            db.query(self.model)
            .filter(Evaluation.notebook_version_id == notebook_version_id)
            .first()
        )

submission = CRUDSubmission(Submission)
notebook_version = CRUDNotebookVersion(NotebookVersion)
evaluation = CRUDEvaluation(Evaluation)
