from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from src.schemas import UserInDBSchema, UserCreateSchema
from src.db_connection import get_db_session
from src.services import user_create_service

auth_router = APIRouter()


@auth_router.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=UserInDBSchema
)
async def create_user(payload: UserCreateSchema, db: Session = Depends(get_db_session)):
    try:
        user = user_create_service(payload=payload, db=db)
    except Exception:
        raise Exception
    return user
