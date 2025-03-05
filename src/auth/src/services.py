from src.schemas import UserCreateSchema, UserInDBSchema
from typing import Union
from sqlalchemy.orm import Session
from src.models import User


def check_existing_user(db: Session, username: str) -> bool:
    try:
        existing_user = db.query(User).filter(User.username == username).first()
    except Exception as e:
        raise e
    return existing_user is not None


def user_create_service(payload: UserCreateSchema, db: Session) -> Union[dict, None]:
    pass
    # valid_return_data = {
    #     "id": "4fe4714f-c85f-40ec-8d85-0f023d2ad468",
    #     "username": "rijojohn",
    # }
    # return UserInDBSchema(**valid_return_data)
