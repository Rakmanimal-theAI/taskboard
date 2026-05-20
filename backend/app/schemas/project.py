from pydantic import BaseModel

class ProjectBase(BaseModel):
    title: str

class ProjectCreateSchema(ProjectBase):
    pass

class ProjectResponseSchema(ProjectBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
