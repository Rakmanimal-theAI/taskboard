import pytest
import sys
import os
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.database import Base
from app.dependencies import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session() -> Generator:
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session) -> Generator:
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def sample_user_data():
    return {
        "email": "test@example.com",
        "name": "testuser",
        "password": "securepassword123"
    }

@pytest.fixture
def sample_project_data():
    return {
        "title": "Test Project",
        "description": "A test project description"
    }

@pytest.fixture
def sample_task_data():
    return {
        "title": "Test Task",
        "priority": "medium",
        "due_date": "2027-05-13T14:30:00"
    }

@pytest.fixture
def registered_user(client, sample_user_data):
    """Register a user and return the response data"""
    response = client.post("/auth/register", json=sample_user_data)
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def auth_headers(client, sample_user_data, registered_user):
    """Register, login, and return auth headers"""
    response = client.post("/auth/login", json={
        "email": sample_user_data["email"],
        "password": sample_user_data["password"]
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def created_project(client, auth_headers, sample_project_data):
    """Create a project and return it"""
    response = client.post("/api/projects", json=sample_project_data, headers=auth_headers)
    assert response.status_code == 200
    return response.json()