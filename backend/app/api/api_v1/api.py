from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, courses, submissions, evaluations

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(submissions.router, prefix="/submissions", tags=["submissions"])
api_router.include_router(evaluations.router, prefix="/evaluations", tags=["evaluations"])
