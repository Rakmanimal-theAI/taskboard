from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum
from typing import Optional

class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskBase(BaseModel):
    title: str
    priority: TaskPriority = TaskPriority.medium
    assignee_id: Optional[int] = None
    due_date: Optional[datetime] = None

class TaskCreateSchema(TaskBase):
    status: Optional[TaskStatus] = TaskStatus.todo

class TaskResponseSchema(TaskBase):
    id: int
    status: TaskStatus = TaskStatus.todo
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)