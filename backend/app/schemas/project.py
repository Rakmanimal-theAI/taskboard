from pydantic import BaseModel
from typing import Optional
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None

class ProjectCreateSchema(ProjectBase):
    pass

class ProjectResponseSchema(ProjectBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
