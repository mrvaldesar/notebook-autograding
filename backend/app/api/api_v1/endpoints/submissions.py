import os
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import shutil

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/assignments/{assignment_id}/submit", response_model=schemas.submission.NotebookVersion)
async def submit_notebook(
    assignment_id: int,
    db: Session = Depends(deps.get_db),
    file: UploadFile = File(...),
    current_user: models.User = Depends(deps.get_current_active_student),
) -> Any:
    """
    Submit a Jupyter notebook for an assignment.
    """
    if not file.filename.endswith(".ipynb"):
        raise HTTPException(status_code=400, detail="Only .ipynb files are allowed")

    assignment = crud.assignment.get(db=db, id=assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    submission = crud.submission.get_by_assignment_and_student(
        db=db, assignment_id=assignment_id, student_id=current_user.id
    )

    if not submission:
        submission = crud.submission.create(
            db=db, obj_in=schemas.submission.SubmissionCreate(
                assignment_id=assignment_id, student_id=current_user.id
            )
        )

    # Determine version number
    versions = crud.notebook_version.get_multi_by_submission(db=db, submission_id=submission.id)
    version_number = len(versions) + 1

    # Save file
    file_path = os.path.join(UPLOAD_DIR, f"student_{current_user.id}_assignment_{assignment_id}_v{version_number}.ipynb")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create NotebookVersion
    notebook_version = crud.notebook_version.create(
        db=db, obj_in=schemas.submission.NotebookVersionCreate(
            submission_id=submission.id, version_number=version_number, file_path=file_path
        )
    )

    # Create empty Evaluation record
    evaluation = crud.evaluation.create(
        db=db, obj_in=schemas.submission.EvaluationCreate(
            notebook_version_id=notebook_version.id, status=models.submission.EvaluationStatus.PENDING
        )
    )

    # Audit log
    crud.audit_log.log_action(
        db=db, evaluation_id=evaluation.id, action=models.audit.AuditActionEnum.EVALUATION_STARTED, details="Submission received and enqueued."
    )

    from app.worker import autograde_notebook
    autograde_notebook.delay(notebook_version.id)

    return notebook_version

@router.post("/assignments/{assignment_id}/testset", response_model=schemas.course.Assignment)
async def upload_hidden_test_set(
    assignment_id: int,
    db: Session = Depends(deps.get_db),
    file: UploadFile = File(...),
    current_user: models.User = Depends(deps.get_current_active_professor),
) -> Any:
    """
    Upload a hidden test set for an assignment.
    """
    assignment = crud.assignment.get(db=db, id=assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    course = crud.course.get(db=db, id=assignment.course_id)
    if course.professor_id != current_user.id:
         raise HTTPException(status_code=400, detail="Not enough permissions")

    test_dir = os.path.join(UPLOAD_DIR, "testsets")
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    safe_filename = os.path.basename(file.filename)
    file_path = os.path.join(test_dir, f"assignment_{assignment_id}_testset_{safe_filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    assignment = crud.assignment.update(
        db=db, db_obj=assignment, obj_in=schemas.course.AssignmentUpdate(hidden_dataset_path=file_path)
    )

    return assignment
