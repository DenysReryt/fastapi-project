from pydantic import BaseModel


class User(BaseModel):
    first_name: str
    last_name: str
    position: str
    email: str

    class Config:
        orm_mode = True


class SignIn(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


class SignUp(BaseModel):
    first_name: str
    last_name: str
    position: str
    email: str
    password: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    position: str
    email: str
    password: str

    class Config:
        orm_mode = True


class UserListResponse(BaseModel):
    first_name: str

    class Config:
        orm_mode = True
