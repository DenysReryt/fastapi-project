from fastapi import APIRouter, HTTPException, Path, Response, status
from typing import List
from src.app.database import database, engine, metadata
from src.app.user_crud import UserCrud as crud
from src.app import schemas

metadata.create_all(bind=engine)

router = APIRouter()


@router.on_event('startup')
async def startup():
    await database.connect()


@router.on_event('shutdown')
async def shutdown():
    await database.disconnect()


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
@router.post('/', response_model=schemas.SignUpSchema)
async def create_user(user: schemas.SignUpSchema):
    db_user = await crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(user=user)


# Update user
@router.put('/{id}', response_model=schemas.UpdateUserSchema)
async def update_user(user: schemas.UpdateUserSchema, id: int = Path(..., gt=0)):
    db_user = await crud.get_user_by_id(id)
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')

    user_id = await crud.update_user(id, user)

    response_object = {
        "id": user_id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role,
    }
    return response_object


# Delete user
@router.delete('/{id}', response_model=schemas.UserBaseSchema)
async def delete_user(id: int = Path(..., gt=0)):
    user = await crud.get_user_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    await crud.delete(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
