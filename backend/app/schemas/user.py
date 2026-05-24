from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreateSchema(UserBase):
    password: str

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserResponseSchema(UserBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)