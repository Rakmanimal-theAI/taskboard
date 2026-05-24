import pytest
from app.models import User, Project, Task
from sqlalchemy.exc import IntegrityError

class TestUserModel:
    def test_create_user(self, db_session):
        user = User(email="john@example.com", name="john_doe", hashed_password="fakehashedpassword123")
        db_session.add(user)
        db_session.commit()
        assert user.id is not None
        assert user.email == "john@example.com"
        assert user.name == "john_doe"

    def test_user_email_unique_constraint(self, db_session):
        user1 = User(email="same@example.com", name="user1", hashed_password="pass")
        user2 = User(email="same@example.com", name="user2", hashed_password="pass")
        db_session.add(user1)
        db_session.commit()
        db_session.add(user2)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()

    def test_user_name_unique_constraint(self, db_session):
        user1 = User(email="email1@test.com", name="sameuser", hashed_password="pass")
        user2 = User(email="email2@test.com", name="sameuser", hashed_password="pass")
        db_session.add(user1)
        db_session.commit()
        db_session.add(user2)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()

    def test_user_project_relationship(self, db_session):
        user = User(email="test@test.com", name="tester", hashed_password="pass")
        db_session.add(user)
        db_session.commit()
        project = Project(title="My Project", description="desc", owner_id=user.id)
        db_session.add(project)
        db_session.commit()
        assert len(user.projects) == 1
        assert user.projects[0].title == "My Project"

class TestProjectModel:
    def test_create_project(self, db_session):
        user = User(email="owner@test.com", name="owner", hashed_password="pass")
        db_session.add(user)
        db_session.commit()
        project = Project(title="Project", description="desc", owner_id=user.id)
        db_session.add(project)
        db_session.commit()
        assert project.id is not None
        assert project.description == "desc"

class TestTaskModel:
    def test_create_task(self, db_session):
        user = User(email="u@test.com", name="u", hashed_password="pass")
        db_session.add(user)
        db_session.commit()
        project = Project(title="P", owner_id=user.id)
        db_session.add(project)
        db_session.commit()
        task = Task(title="Task 1", priority="medium", project_id=project.id)
        db_session.add(task)
        db_session.commit()
        assert task.id is not None
        assert task.status == "todo"