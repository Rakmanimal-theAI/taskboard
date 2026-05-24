import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Test database (use separate DB for testing)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # or postgresql://test:test@localhost/test_db
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session() -> Generator:
    """Create a fresh database session for each test"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create a new session
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    
    # Clean up after test
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session) -> Generator:
    """Create a test client with overridden database dependency"""
    
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
def sample_user_register_data():
    """Sample data for user registration tests"""
    return {
        "email": "test@example.com",
        "name": "testuser",
        "password": "securepassword123"
    }

@pytest.fixture
def sample_user_login_data():
    """Sample data for user login tests"""
    return {
        "email": "test@example.com",
        "password": "securepassword123"
    }

@pytest.fixture
def sample_project_data():
    """Sample data for creating project via API"""
    return {
        "title": "Dashboard project",
        "description": "This project is a full-stack project to deal with projects and tasks progression."
    }

@pytest.fixture
def sample_project_data():
    """Sample data for creating project via API"""
    return {
        "title": "Dashboard project",
        "description": "This project is a full-stack project to deal with projects and tasks progression."
    }

@pytest.fixture
def sample_task_data():
    """Sample data for creating task via API"""
    return {
        "title": "First task",
        "priority": "in_progress",
        "assignee_id": "1",
        "due_date": "2027-05-13T14:30:00"
    }