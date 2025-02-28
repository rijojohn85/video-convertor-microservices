import os
import pytest
import docker

from src.main import app
from tests.utils.docker_utils import start_database_container
from tests.utils.database_utils import migrate_to_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def db_session():
    container: docker.DockerClient = start_database_container()
    env = os.getenv("TEST_DATABASE_URL")
    if not env:
        raise ValueError("env vars not set.")
    engine = create_engine(env)

    with engine.begin() as connection:
        migrate_to_db("migrations", "alembic.ini", connection)
    SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

    yield SessionLocal

    container.stop()
    container.remove(force=True)
    engine.dispose()

@pytest.fixture(scope="function")
def client():
    with TestClient(app) as client:
        yield client