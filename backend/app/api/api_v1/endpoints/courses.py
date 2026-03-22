from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.course.Course])
def read_courses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve courses.
    """
    if crud.user.is_professor(current_user):
        courses = crud.course.get_multi_by_owner(
            db=db, professor_id=current_user.id, skip=skip, limit=limit
        )
    else:
        courses = crud.enrollment.get_enrolled_courses(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )
    return courses

@router.post("/", response_model=schemas.course.Course)
def create_course(
    *,
    db: Session = Depends(deps.get_db),
    course_in: schemas.course.CourseCreate,
    current_user: models.User = Depends(deps.get_current_active_professor),
) -> Any:
    """
    Create new course.
    """
    course = crud.course.create_with_owner(
        db=db, obj_in=course_in, professor_id=current_user.id
    )
    return course

@router.get("/{course_id}/assignments", response_model=List[schemas.course.Assignment])
def read_assignments(
    course_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get assignments for a specific course.
    """
    course = crud.course.get(db=db, id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # TODO: Verify if student is enrolled or if current_user is the professor
    assignments = crud.assignment.get_multi_by_course(
        db=db, course_id=course_id, skip=skip, limit=limit
    )
    return assignments

@router.post("/{course_id}/assignments", response_model=schemas.course.Assignment)
def create_assignment(
    *,
    course_id: int,
    db: Session = Depends(deps.get_db),
    assignment_in: schemas.course.AssignmentBase,
    current_user: models.User = Depends(deps.get_current_active_professor),
) -> Any:
    """
    Create new assignment.
    """
    course = crud.course.get(db=db, id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.professor_id != current_user.id:
         raise HTTPException(status_code=400, detail="Not enough permissions")

    assignment_create = schemas.course.AssignmentCreate(**assignment_in.dict(), course_id=course_id)
    assignment = crud.assignment.create(db=db, obj_in=assignment_create)
    return assignment

@router.get("/assignments/{assignment_id}/rubric", response_model=schemas.course.Rubric)
def read_rubric(
    assignment_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    rubric = crud.rubric.get_by_assignment(db=db, assignment_id=assignment_id)
    if not rubric:
        raise HTTPException(status_code=404, detail="Rubric not found")
    return rubric

@router.post("/assignments/{assignment_id}/rubric", response_model=schemas.course.Rubric)
def create_rubric(
    *,
    assignment_id: int,
    db: Session = Depends(deps.get_db),
    rubric_in: schemas.course.RubricBase,
    current_user: models.User = Depends(deps.get_current_active_professor),
) -> Any:
    assignment = crud.assignment.get(db=db, id=assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    course = crud.course.get(db=db, id=assignment.course_id)
    if course.professor_id != current_user.id:
         raise HTTPException(status_code=400, detail="Not enough permissions")

    existing_rubric = crud.rubric.get_by_assignment(db=db, assignment_id=assignment_id)
    if existing_rubric:
         raise HTTPException(status_code=400, detail="Rubric already exists")

    rubric_create = schemas.course.RubricCreate(**rubric_in.dict(), assignment_id=assignment_id)
    rubric = crud.rubric.create(db=db, obj_in=rubric_create)
    return rubric
