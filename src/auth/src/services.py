from src.schemas import UserCreateSchema, UserInDBSchema
from sqlalchemy.orm import Session


def user_create_service(payload: UserCreateSchema, db: Session) -> UserInDBSchema:
    valid_return_data = {
        "id": "4fe4714f-c85f-40ec-8d85-0f023d2ad468",
        "username": "rijojohn",
    }
    return UserInDBSchema(**valid_return_data)
