from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/assignments/{assignment_id}/submissions", response_model=List[schemas.submission.Submission])
def read_submissions_for_assignment(
    assignment_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_professor),
) -> Any:
    """
    Retrieve all submissions for a specific assignment.
    """
    assignment = crud.assignment.get(db=db, id=assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    course = crud.course.get(db=db, id=assignment.course_id)
    if course.professor_id != current_user.id:
         raise HTTPException(status_code=400, detail="Not enough permissions")

    submissions = db.query(models.Submission).filter(models.Submission.assignment_id == assignment_id).offset(skip).limit(limit).all()
    return submissions

@router.get("/submissions/{submission_id}/versions", response_model=List[schemas.submission.NotebookVersion])
def read_submission_versions(
    submission_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve version history for a submission.
    """
    submission = crud.submission.get(db=db, id=submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    if crud.user.is_student(current_user) and submission.student_id != current_user.id:
         raise HTTPException(status_code=400, detail="Not enough permissions")

    if crud.user.is_professor(current_user):
        assignment = crud.assignment.get(db=db, id=submission.assignment_id)
        course = crud.course.get(db=db, id=assignment.course_id)
        if course.professor_id != current_user.id:
            raise HTTPException(status_code=400, detail="Not enough permissions")

    versions = crud.notebook_version.get_multi_by_submission(db=db, submission_id=submission_id, skip=skip, limit=limit)
    return versions

@router.get("/notebook_versions/{notebook_version_id}/evaluation", response_model=schemas.submission.Evaluation)
def read_evaluation(
    notebook_version_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve evaluation for a specific notebook version.
    """
    version = crud.notebook_version.get(db=db, id=notebook_version_id)
    if not version:
        raise HTTPException(status_code=404, detail="Notebook version not found")

    submission = crud.submission.get(db=db, id=version.submission_id)

    if crud.user.is_student(current_user) and submission.student_id != current_user.id:
         raise HTTPException(status_code=400, detail="Not enough permissions")

    if crud.user.is_professor(current_user):
        assignment = crud.assignment.get(db=db, id=submission.assignment_id)
        course = crud.course.get(db=db, id=assignment.course_id)
        if course.professor_id != current_user.id:
            raise HTTPException(status_code=400, detail="Not enough permissions")

    evaluation = crud.evaluation.get_by_notebook_version(db=db, notebook_version_id=notebook_version_id)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return evaluation
