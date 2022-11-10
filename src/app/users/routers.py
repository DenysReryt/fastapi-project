from fastapi import APIRouter, HTTPException, Path, status, Depends

from typing import List

from src.app.database import engine, metadata
from src.app.users.user_crud import crud

from src.app import schemas

from src.app.auth0.utils import get_current_user, get_email_from_token

metadata.create_all(bind=engine)

router = APIRouter()


# Get all users
@router.get('/', response_model=List[schemas.ListUsersResponse])
async def get_all_users(skip: int = 0, limit: int = 100) -> List[schemas.ListUsersResponse]:
    return await crud.get_users(skip=skip, limit=limit)


# Get user
@router.get('/{id}', response_model=schemas.UserResponse)
async def get_user(id: int = Path(..., gt=0)) -> schemas.UserResponse:
    user = await crud.get_user_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


# Create user
@router.post('/create', response_model=schemas.UserBaseSchema)
async def create_user(user: schemas.SignUpSchema) -> schemas.UserBaseSchema:
    db_user = await crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(user=user)


# Update user
@router.put('/update', response_model=schemas.UserBaseSchema)
async def update_user(user: schemas.UpdateUserSchema,
                      email: str = Depends(get_email_from_token)) -> schemas.UserBaseSchema:
    if user.email == email:
        return await crud.update_user(user)
    raise HTTPException(status_code=400, detail='No user with this email or no permission to execute')


# Delete user
@router.delete('/delete', status_code=status.HTTP_200_OK)
async def delete_user(user: schemas.DeleteUser, email: str = Depends(get_email_from_token),
                      id: schemas.UserResponse = Depends(get_current_user)) -> HTTPException:
    if user.email == email:
        await crud.delete(email=email, id=id.id)
        raise HTTPException(status_code=200, detail='User has been deleted')
    raise HTTPException(status_code=400, detail='No user was found')
