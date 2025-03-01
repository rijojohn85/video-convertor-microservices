import pytest
from uuid import UUID
from typing import Dict
from pydantic import ValidationError
from fastapi.testclient import TestClient


from src.schemas import UserCreateSchema, UserInDBSchema


def test_unit_schema_create_user_validation() -> None:
    """
    checks that the schema used to accept data for user creation is correct
    """
    valid_data = {
        "username": "rijojohn",
        "password": "rijojohn85",
    }

    user = UserCreateSchema(**valid_data)
    assert user.username == valid_data["username"]
    assert user.password == valid_data["password"]

    invalid_data_no_username = {
        "password": "rijojohn85",
    }
    with pytest.raises(ValidationError):
        _ = UserCreateSchema(**invalid_data_no_username)

    invalid_data_no_password = {
        "username": "rijojohn85",
    }
    with pytest.raises(ValidationError):
        _ = UserCreateSchema(**invalid_data_no_password)

    invalid_data = {
        "abs": "rijojohn85",
    }
    with pytest.raises(ValidationError):
        _ = UserCreateSchema(**invalid_data)


def test_unit_schema_user_indb_validation() -> None:
    """
    checks that the schema used to return data for user creation is correct
    """
    valid_data = {
        "id": UUID("4fe4714f-c85f-40ec-8d85-0f023d2ad468"),
        "username": "rijojohn",
    }
    user = UserInDBSchema(**valid_data)

    assert user.id == valid_data["id"]
    assert user.username == valid_data["username"]

    invalid_data_array = [
        {"username": "rijojohn"},
        {"id": UUID("4fe4714f-c85f-40ec-8d85-0f023d2ad468")},
        {"abc": "abc"},
    ]
    for data in invalid_data_array:
        with pytest.raises(ValidationError):
            _ = UserInDBSchema(**data)


def mock_output(return_value=None):
    return lambda *args, **kwargs: return_value


def test_unit_create_user_route(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    valid_return_data = {
        "id": UUID("4fe4714f-c85f-40ec-8d85-0f023d2ad468"),
        "username": "rijojohn",
    }

    def mock_user_create_service(user_payload: UserCreateSchema) -> UserInDBSchema:
        return UserInDBSchema(**valid_return_data)

    user = UserCreateSchema(username="rijojohn", password="rijojohn85")
