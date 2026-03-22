from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.core import security
from app.core.emails import send_invitation_email
from datetime import timedelta

router = APIRouter()

@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_professor),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users

@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user

@router.post("/invite", response_model=dict)
def invite_user(
    *,
    db: Session = Depends(deps.get_db),
    email: EmailStr = Body(...),
    current_user: models.User = Depends(deps.get_current_active_professor),
) -> Any:
    """
    Invite new user. Generates a token and sends an email.
    """
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    expires = timedelta(days=7)
    token = security.create_access_token(email, expires_delta=expires)

    try:
        send_invitation_email(email_to=email, token=token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")

    return {"msg": "Invitation sent successfully."}

@router.post("/register", response_model=schemas.User)
def register_user(
    *,
    db: Session = Depends(deps.get_db),
    token: str = Body(...),
    user_in: schemas.UserRegister,
) -> Any:
    """
    Register user via invitation token.
    """
    from jose import jwt, JWTError
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

    if email != user_in.email:
         raise HTTPException(status_code=400, detail="Token email does not match user email")

    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    user_create = schemas.UserCreate(
        email=user_in.email,
        password=user_in.password,
        full_name=user_in.full_name,
        role=models.user.RoleEnum.STUDENT,
        student_id=user_in.student_id,
        is_active=True
    )

    user = crud.user.create(db, obj_in=user_create)
    return user

@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user
