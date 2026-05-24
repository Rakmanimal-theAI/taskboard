from pydantic import BaseModel, ConfigDict
from typing import Optional
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None

class ProjectCreateSchema(ProjectBase):
    pass

class ProjectResponseSchema(ProjectBase):
    id: int
    owner_id: int
    model_config = ConfigDict(from_attributes=True)
