from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr, constr


class UserBaseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    role: str = 'user'
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    # if you`re working with db directly (take some information from db)
    class Config:
        orm_mode = True


class SignInUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class SignUpSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: constr(min_length=8)
    role: str = 'user'
    verified: bool = False


class UpdateUserSchema(SignInUserSchema):
    first_name: str
    last_name: str
    role: str = 'user'
    password: constr(min_length=8)

    class Config:
        orm_mode = True


class UserResponse(UserBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class ListUsersResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    created_at: datetime


class DeleteUser(BaseModel):
    email: EmailStr
