from fastapi import APIRouter, HTTPException, status, Depends


from src.app.database import engine, metadata
from src.app.users.user_crud import crud

from src.app import schemas

from src.app.config import settings
from src.app.auth0.utils import create_access_token, get_current_user, set_up, auth_request

from datetime import timedelta

metadata.create_all(bind=engine)

router = APIRouter()


#Get user info
@router.get("/users/login/me")
def get_me(user: schemas.UserBaseSchema = Depends(get_current_user)) -> schemas.UserBaseSchema:
    return user


#Sign In
@router.post("/users/login/", status_code=status.HTTP_200_OK)
async def sign_in_my(user: schemas.SignInUserSchema) -> HTTPException:
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


#Sign Up
@router.post("/users/register/", status_code=status.HTTP_200_OK)
async def sign_up_my(user: schemas.SignUpSchema) -> HTTPException:
    does_exist = await crud.get_user_by_email(email=user.email)
    if does_exist:
        raise HTTPException(status_code=400, detail="Email already registered")
    config = set_up()
    auth_request(config=config, user=user)

    user = await crud.create_user(user)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = await create_access_token(user.email, expires_delta=access_token_expires)
    return token

