import pytest
from uuid import UUID
from typing import Dict
from pydantic import ValidationError
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.main import api_version
from fastapi import status
from src.services import user_create_service, check_existing_user


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
        "id": "4fe4714f-c85f-40ec-8d85-0f023d2ad468",
        "username": "rijojohn",
    }
    user = UserInDBSchema(**valid_data)

    assert user.id == valid_data["id"]
    assert user.username == valid_data["username"]

    invalid_data_array = [
        {"username": "rijojohn"},
        {"id": "4fe4714f-c85f-40ec-8d85-0f023d2ad468"},
        {"abc": "abc"},
    ]
    for data in invalid_data_array:
        with pytest.raises(ValidationError):
            _ = UserInDBSchema(**data)


def mock_output(return_value=None):
    return lambda *args, **kwargs: return_value


def test_unit_create_user_route(client: TestClient) -> None:
    valid_return_data = {
        "id": "4fe4714f-c85f-40ec-8d85-0f023d2ad468",
        "username": "rijojohn",
    }

    valid_input_data = {
        "username": "rijojohn",
        "password": "rijojohn85",
    }

    with patch(
        "src.routes.user_create_service",
        return_value=valid_return_data,
    ):
        response = client.post(f"/api/{api_version}/users", json=valid_input_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == valid_return_data


def test_unit_create_user_invalid_data(client: TestClient) -> None:
    invalid_data_list = [
        {"username": "rijojohn"},
        {"password": "rijojohn85"},
        {"abc": "xyz"},
    ]
    for data in invalid_data_list:
        response = client.post(f"/api/{api_version}/users", json=data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_unit_create_user_service_success(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    valid_input_data = {
        "username": "rijojohn",
        "password": "rijojohn85",
    }

    def mock_check_existing_user(_db, _username):
        return False

    monkeypatch.setattr("src.service.check_existing_user", mock_check_existing_user)
    monkeypatch.setattr("sqlalchemy.orm.Session.add", mock_output)
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_output)
    monkeypatch.setattr("sqlalchemy.orm.Session.refresh", mock_output)

    response = user_create_service()
