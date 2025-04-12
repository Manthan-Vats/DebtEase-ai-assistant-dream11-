from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Shared properties


class UserBase(BaseModel):
    email: EmailStr

# Properties to receive via API on creation


class UserCreate(UserBase):
    password: str

# Properties to receive via API on update


class UserUpdate(UserBase):
    password: Optional[str] = None

# Properties shared by models stored in DB


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

# Additional properties to return via API


class User(UserInDBBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Additional properties stored in DB


class UserInDB(UserInDBBase):
    hashed_password: str
