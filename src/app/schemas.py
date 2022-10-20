from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, EmailStr, constr


class UserBaseSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        orm_mode = True


class SignInUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class SignUpSchema(UserBaseSchema):
    password: constr(min_length=8)
    # passwordConfirm: str
    role: str = 'user'
    verified: bool = False


class UpdateUserSchema(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    role: str = 'user'
    updated_at: datetime

    class Config:
        orm_mode = True


class UserResponse(UserBaseSchema):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ListUsersResponse(BaseModel):
    status: str
    results: int
    users: List[UserResponse]

