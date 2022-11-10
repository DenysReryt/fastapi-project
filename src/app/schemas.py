from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, constr


class UserBaseSchema(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
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


## Companies
class ListCompanies(BaseModel):
    id: int
    name: str = 'name'
    description: str = 'description'
    owner_id: int


class CompanyBaseSchema(BaseModel):
    id: int
    visibility: bool = True
    name: str = 'name'
    description: str
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class CompanyMain(BaseModel):
    visibility: bool = True
    name: str = 'name'
    description: str = 'description'


## Invitations
class Invitation(BaseModel):
    id: int
    user_id: int
    company_id: int
    status: str = 'on review'


class UsersOfCompany(BaseModel):
    user_id: int
    is_admin: bool = False


class ListInvitations(BaseModel):
    user_id: int
    status: str = 'on review'


class ListInvitationsCompanies(BaseModel):
    company_id: int
    status: str = 'on review'


##Quizzes
class BaseQuiz(BaseModel):
    id: int
    company_id: int
    name: str
    description: str
    frequency: int
    created_at: datetime

    class Config:
        orm_mode = True


class CreateQuiz(BaseModel):
    name: str
    description: str
    frequency: int


class ListQuizzes(BaseModel):
    id: int
    company_id: int
    name: str
    description: str


class BaseQuestion(BaseModel):
    question_id: int
    quiz_id: int
    question: str

    class Config:
        orm_mode = True


class CreateQuestion(BaseModel):
    question: str


class ListQuestion(BaseModel):
    question_id: int
    question: str


## Results
class BaseResult(BaseModel):
    id: int
    user_id: int
    company_id: int
    quiz_id: int
    result: float
    time: datetime


class AnswerInput(BaseModel):
    question_id: int = 1
    answer: str = ''


class QuizResult(BaseModel):
    result: float


class Rating(BaseModel):
    user_id: int
    rating: float


#Analytics
class ListOfUserResults(BaseModel):
    user_id: int
    time: datetime
