from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from app.models.course import DockerEnvEnum

# Course Schemas
class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass

class CourseInDBBase(CourseBase):
    id: int
    professor_id: int

    class Config:
        from_attributes = True

class Course(CourseInDBBase):
    pass

# Assignment Schemas
class AssignmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    docker_env: Optional[DockerEnvEnum] = DockerEnvEnum.BASIC

class AssignmentCreate(AssignmentBase):
    course_id: int

class AssignmentUpdate(AssignmentBase):
    pass

class AssignmentInDBBase(AssignmentBase):
    id: int
    course_id: int
    hidden_dataset_path: Optional[str] = None

    class Config:
        from_attributes = True

class Assignment(AssignmentInDBBase):
    pass

# Rubric Schemas
class RubricBase(BaseModel):
    criteria: List[Dict[str, Any]]

class RubricCreate(RubricBase):
    assignment_id: int

class RubricUpdate(RubricBase):
    pass

class RubricInDBBase(RubricBase):
    id: int
    assignment_id: int

    class Config:
        from_attributes = True

class Rubric(RubricInDBBase):
    pass

# Enrollment Schemas
class EnrollmentCreate(BaseModel):
    user_id: int
    course_id: int

class Enrollment(BaseModel):
    id: int
    user_id: int
    course_id: int
    enrolled_at: datetime

    class Config:
        from_attributes = True
