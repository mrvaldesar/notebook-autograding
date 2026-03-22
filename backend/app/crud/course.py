from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.course import Course, Assignment, Rubric, Enrollment
from app.schemas.course import CourseCreate, CourseUpdate, AssignmentCreate, AssignmentUpdate, RubricCreate, RubricUpdate, EnrollmentCreate

class CRUDCourse(CRUDBase[Course, CourseCreate, CourseUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: CourseCreate, professor_id: int
    ) -> Course:
        db_obj = Course(
            title=obj_in.title,
            description=obj_in.description,
            professor_id=professor_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, professor_id: int, skip: int = 0, limit: int = 100
    ) -> List[Course]:
        return (
            db.query(self.model)
            .filter(Course.professor_id == professor_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

class CRUDAssignment(CRUDBase[Assignment, AssignmentCreate, AssignmentUpdate]):
    def get_multi_by_course(
        self, db: Session, *, course_id: int, skip: int = 0, limit: int = 100
    ) -> List[Assignment]:
        return (
            db.query(self.model)
            .filter(Assignment.course_id == course_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

class CRUDRubric(CRUDBase[Rubric, RubricCreate, RubricUpdate]):
    def get_by_assignment(
        self, db: Session, *, assignment_id: int
    ) -> Optional[Rubric]:
        return (
            db.query(self.model)
            .filter(Rubric.assignment_id == assignment_id)
            .first()
        )

class CRUDEnrollment(CRUDBase[Enrollment, EnrollmentCreate, EnrollmentCreate]):
    def get_enrolled_courses(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Course]:
        return (
            db.query(Course)
            .join(Enrollment, Course.id == Enrollment.course_id)
            .filter(Enrollment.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

course = CRUDCourse(Course)
assignment = CRUDAssignment(Assignment)
rubric = CRUDRubric(Rubric)
enrollment = CRUDEnrollment(Enrollment)
