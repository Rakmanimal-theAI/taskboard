import pytest
from pydantic import ValidationError
from app.schemas.user import UserCreateSchema, UserResponseSchema
from app.schemas.project import ProjectCreateSchema, ProjectResponseSchema
from app.schemas.task import TaskCreateSchema, TaskResponseSchema, TaskPriority

class TestUserSchemas:
    def test_valid_user_create(self):
        user = UserCreateSchema(email="user@example.com", name="validuser", password="pass123")
        assert user.email == "user@example.com"
        assert user.name == "validuser"

    def test_invalid_email(self):
        with pytest.raises(ValidationError):
            UserCreateSchema(email="notanemail", name="user", password="pass123")

    def test_missing_required_fields(self):
        with pytest.raises(ValidationError):
            UserCreateSchema(email="user@example.com")

class TestProjectSchemas:
    def test_valid_project_create(self):
        project = ProjectCreateSchema(title="My Project", description="desc")
        assert project.title == "My Project"
        assert project.description == "desc"

    def test_description_optional(self):
        project = ProjectCreateSchema(title="No desc project")
        assert project.description is None

    def test_missing_title(self):
        with pytest.raises(ValidationError):
            ProjectCreateSchema(description="no title")

class TestTaskSchemas:
    def test_valid_task_create(self):
        task = TaskCreateSchema(title="Fix bug", priority="high")
        assert task.title == "Fix bug"
        assert task.priority == TaskPriority.high

    def test_invalid_priority(self):
        with pytest.raises(ValidationError):
            TaskCreateSchema(title="Task", priority="urgent")

    def test_optional_fields(self):
        task = TaskCreateSchema(title="Minimal task", priority="low")
        assert task.due_date is None
        assert task.assignee_id is None