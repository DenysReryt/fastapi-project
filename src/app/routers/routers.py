from fastapi import APIRouter, HTTPException, Path, Response, status, Depends

from typing import List

import http.client

from src.app.database import engine, metadata
from src.app.user_crud import crud
from src.app import schemas

from src.app.config import settings
from src.app.auth0.utils import create_access_token, get_current_user, set_up, get_email_from_token, auth_request

from datetime import timedelta

metadata.create_all(bind=engine)

router = APIRouter()


@router.get("/login/me", tags=["auth"])
def get_me(user: schemas.UserBaseSchema = Depends(get_current_user)):
    return user

@router.post("/login/", tags=["auth"], status_code=status.HTTP_200_OK)
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

@router.post("/register/", tags=["auth"], status_code=status.HTTP_200_OK)
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
@router.get('/', response_model=List[schemas.ListUsersResponse])
async def get_all_users(skip: int = 0, limit: int = 100):
    return await crud.get_users(skip=skip, limit=limit)


# Get user
@router.get('/{id}', response_model=schemas.UserResponse)
async def get_user(id: int = Path(..., gt=0)):
    user = await crud.get_user_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


# Create user
@router.post('/', response_model=schemas.UserBaseSchema)
async def create_user(user: schemas.SignUpSchema):
    db_user = await crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(user=user)


# Update user
@router.put('/update', response_model=schemas.UserBaseSchema)
async def update_user(user: schemas.UpdateUserSchema, email: str = Depends(get_email_from_token)):
    if user.email == email:
        return await crud.update_user(user)
    raise HTTPException(status_code=400, detail='No user with this email or no permission to execute')


# Delete user
@router.delete('/delete', status_code=status.HTTP_200_OK)
async def delete_user(user: schemas.DeleteUser, email: str = Depends(get_email_from_token)):
    if user.email == email:
        await crud.delete(email)
        return HTTPException(status_code=200, detail='User has been deleted')
    return HTTPException(status_code=400, detail='No user was found')
