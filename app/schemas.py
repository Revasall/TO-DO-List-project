from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# --- Users schemas ---
class UserBase(BaseModel):
    username: str = Field(max_length=20)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(max_length=20)


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserUpdate(UserBase): 
    username: str | None = Field(default=None, max_length=20)
    email: EmailStr | None = None
    password: str = Field(default=None, max_length=20)


# --- Task schemas ---
class TaskBase(BaseModel):

    title: str = Field(max_length=100)
    description: str | None = Field(default=None, max_length=1000)
    deadline: datetime | None = None
    priority: int | None = Field(default=0, ge=0, le=5)

class TaskSummary(BaseModel):
    id: int
    title: str
    deadline: datetime

class TaskCreate(TaskBase):...


class TaskRead(TaskBase):
    id: int
    created_at: datetime
    done: bool
    completed_at: datetime | None = None
    owner_id: int


    class Config:
        from_attributes = True


class TaskUpdate(TaskBase):
    title: str|None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=1000)
    deadline: datetime | None = None
    done: bool | None = None

TaskRead.model_rebuild()
UserRead.model_rebuild()

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
