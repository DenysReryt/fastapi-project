from datetime import datetime
import uuid
from src.app import models, schemas
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from src.app.database import get_db

router = APIRouter()


# Get all Users
@router.get('/', response_model=schemas.ListUsersResponse)
async def get_users(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit

    users = db.query(models.User).group_by(models.User.id).filter(
        models.User.last_name.contains(search)).limit(limit).offset(skip).all()
    return {'status': 'success', 'result': len(users), 'users': users}


# Create user
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.SignUpSchema, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Update user
@router.put('/{id}', response_model=schemas.UserResponse)
async def update_user(id: str, user: schemas.UpdateUserSchema, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    db_user = user_query.first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_200_OK, detail=f'No user with this id: {id} found')
    if db_user.id != uuid.UUID(id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to perform this action!')
    user.id = db_user.id
    user.updated_at = db_user.updated_at
    user_query.update(user.dict(exclude_none=True), synchronize_session=False)
    db.commit()
    return db_user


# Get one user
@router.get('/{id}', response_model=schemas.UserResponse)
async def get_user(id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this id: {id} found')
    return user


# Delete user
@router.delete('/{id}')
async def delete_user(id: str, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this id: {id} found')
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
