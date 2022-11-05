from fastapi import APIRouter, HTTPException, Path, Response, status, Depends

from typing import List

import http.client

from src.app.database import engine, metadata
from src.app.user_crud import crud
from src.app.companies.company_crud import company_crud
from src.app import schemas

from src.app.config import settings
from src.app.auth0.utils import create_access_token, get_current_user, set_up, get_email_from_token, auth_request

from datetime import timedelta

metadata.create_all(bind=engine)

router = APIRouter()


@router.get("/users/login/me", tags=["auth"])
def get_me(user: schemas.UserBaseSchema = Depends(get_current_user)):
    return user

@router.post("/users/login/", tags=["auth"], status_code=status.HTTP_200_OK)
async def sign_in_my(user: schemas.SignInUserSchema):
    user_check = await crud.get_user_by_email(user.email)
    if user_check:
        if user_check.password == user.password:
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            token = await create_access_token(user.email, expires_delta=access_token_expires)
            return token
        else:
            raise HTTPException(status_code=400, detail='Incorrect password')
    else:
        raise HTTPException(status_code=400, detail="No such user or incorrect email")

@router.post("/users/register/", tags=["auth"], status_code=status.HTTP_200_OK)
async def sign_up_my(user: schemas.SignUpSchema):
    does_exist = await crud.get_user_by_email(email=user.email)
    if does_exist:
        raise HTTPException(status_code=400, detail="Email already registered")
    config = set_up()
    auth_request(config=config, user=user)

    user = await crud.create_user(user)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = await create_access_token(user.email, expires_delta=access_token_expires)
    return token


# Get all users
@router.get('/users/', tags=['Users'], response_model=List[schemas.ListUsersResponse])
async def get_all_users(skip: int = 0, limit: int = 100):
    return await crud.get_users(skip=skip, limit=limit)


# Get user
@router.get('/users/{id}', tags=['Users'], response_model=schemas.UserResponse)
async def get_user(id: int = Path(..., gt=0)):
    user = await crud.get_user_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


# Create user
@router.post('/users/', tags=['Users'], response_model=schemas.UserBaseSchema)
async def create_user(user: schemas.SignUpSchema):
    db_user = await crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(user=user)


# Update user
@router.put('/users/update', tags=['Users'], response_model=schemas.UserBaseSchema)
async def update_user(user: schemas.UpdateUserSchema, email: str = Depends(get_email_from_token)):
    if user.email == email:
        return await crud.update_user(user)
    raise HTTPException(status_code=400, detail='No user with this email or no permission to execute')


# Delete user
@router.delete('/users/delete', tags=['Users'], status_code=status.HTTP_200_OK)
async def delete_user(user: schemas.DeleteUser, email: str = Depends(get_email_from_token)):
    if user.email == email:
        await crud.delete(email)
        return HTTPException(status_code=200, detail='User has been deleted')
    return HTTPException(status_code=400, detail='No user was found')


# Create company
@router.post('/companies/', tags=['Companies'], response_model=schemas.CompanyBaseSchema)
async def create_company(company: schemas.MainCompany, owner: schemas.UserBaseSchema = Depends(get_current_user)):
    return await company_crud.create_company(company=company, owner=owner.id)


#Update company
@router.put('/companies/update{company_id}', tags=['Companies'], response_model=schemas.CompanyBaseSchema)
async def update_comapny(company: schemas.MainCompany, company_id: int = Path(..., gt=0), user: schemas.UserBaseSchema = Depends(get_current_user)):
    company_id = await company_crud.get_company_by_id(company_id)
    if not company_id:
        raise HTTPException(status_code=404, detail='Company not found')
    return await company_crud.update_company(company=company, company_id=company_id)
