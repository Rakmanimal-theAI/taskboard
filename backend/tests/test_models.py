import pytest
from app.models import User, Project, Task
from sqlalchemy.exc import IntegrityError

class TestUserModel:
    """Test User model"""
    
    def test_create_user(self, db_session):
        """Test creating a valid user"""
        user = User(
            email="john@example.com",
            name="john_doe",
            hashed_password="fakehashedpassword123"
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.email == "john@example.com"
        assert user.name == "john_doe"
        assert user.created_at is not None
    
    def test_user_email_unique_constraint(self, db_session):
        """Test that email must be unique"""
        user1 = User(email="same@example.com", name="user1", hashed_password="pass")
        user2 = User(email="same@example.com", name="user2", hashed_password="pass")
        
        db_session.add(user1)
        db_session.commit()
        db_session.add(user2)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
    
    def test_user_name_unique_constraint(self, db_session):
        """Test that username must be unique"""
        user1 = User(email="email1@test.com", name="sameuser", hashed_password="pass")
        user2 = User(email="email2@test.com", name="sameuser", hashed_password="pass")
        
        db_session.add(user1)
        db_session.commit()
        db_session.add(user2)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
    
    def test_user_project_relationships(self, db_session):
        """Test relationship with projects"""
        user = User(email="test@test.com", name="tester", hashed_password="pass")
        db_session.add(user)
        db_session.commit()
        
        project = Project(title="Title", description="Project description", owner_id=user.id)
        db_session.add(project)
        db_session.commit()
        
        assert len(user.projects) == 1
        assert user.projects[0].title == "Title"