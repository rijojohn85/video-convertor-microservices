from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas import UserInDBSchema, UserCreateSchema
from src.db_connection import get_db_session
from src.services import user_create_service, check_existing_user

auth_router = APIRouter()


@auth_router.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=UserInDBSchema
)
async def create_user(payload: UserCreateSchema, db: Session = Depends(get_db_session)):
    try:
        user = user_create_service(payload=payload, db=db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    response_user = UserInDBSchema(**user)

    return response_user
