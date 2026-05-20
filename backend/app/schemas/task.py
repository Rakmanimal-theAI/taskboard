from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional

class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class TaskBase(BaseModel):
    title: str
    priority: str
    assignee_id: Optional[int] = None
    due_date: Optional[datetime] = None

class TaskCreateSchema(TaskBase):
    pass

class TaskResponseSchema(TaskBase):
    id: int
    status: TaskStatus = TaskStatus.todo
    project_id: int

    class Config:
        from_attributes = True