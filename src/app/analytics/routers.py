from fastapi import APIRouter, HTTPException, Path, Depends

from typing import List

from src.app.database import engine, metadata
from src.app.analytics.analytic_crud import analytic_crud
from src.app.invitations.invitation_crud_for_companies import inv_crud
from src.app.users.user_crud import crud
from src.app.companies.company_crud import company_crud
from src.app import schemas
from src.app.result import user_result

from src.app.auth0.utils import get_current_user

metadata.create_all(bind=engine)

router = APIRouter()


# Get analytic of users
@router.get('/users/{company_id}', response_model=List[schemas.ListOfUsersResults])
async def get_users(user: schemas.UserBaseSchema = Depends(get_current_user),
                    company_id: int = Path(..., gt=0)) -> List[schemas.ListOfUserResults]:
    get_company = await company_crud.get_company_by_id(company_id)
    if not get_company:
        raise HTTPException(status_code=404, detail='Company not found')
    check_admin = await inv_crud.get_status_admin(company_id=company_id, user_id=user.id)
    if get_company.owner_id == user.id:
        return await analytic_crud.get_users_results(company_id=company_id)
    if get_company.owner_id != user.id and not check_admin:
        raise HTTPException(status_code=403, detail='You are not the owner or admin')
    return await analytic_crud.get_user_results(company_id=company_id)


# Get analytic of user
@router.get('/user/{user_id}/{company_id}', response_model=List[schemas.ListOfUserResults])
async def get_user(user: schemas.UserBaseSchema = Depends(get_current_user), user_id: int = Path(..., gt=0),
                   company_id: int = Path(..., gt=0)) -> List[schemas.ListOfUserResults]:
    get_company = await company_crud.get_company_by_id(company_id)
    if not get_company:
        raise HTTPException(status_code=404, detail='Company not found')
    check_admin = await inv_crud.get_status_admin(company_id=company_id, user_id=user.id)
    get_user = await analytic_crud.get_user_results(user_id=user_id, company_id=company_id)
    if not get_user:
        raise HTTPException(status_code=400, detail='the user was not found or the user did not pass any quiz')
    if get_company.owner_id == user.id:
        return await analytic_crud.get_user_results(user_id=user_id, company_id=company_id)
    if get_company.owner_id != user.id and not check_admin:
        raise HTTPException(status_code=403, detail='You are not the owner or admin')
    return await analytic_crud.get_user_results(user_id=user_id, company_id=company_id)


# Get user last time
@router.get('/last_time/{company_id}', status_code=200)
async def last_time_pass(user: schemas.UserBaseSchema = Depends(get_current_user),
                         company_id: int = Path(..., gt=0)) -> schemas.ListOfUserResults:
    get_company = await company_crud.get_company_by_id(company_id)
    get_users = await analytic_crud.get_users_results(company_id=company_id)
    if not get_company:
        raise HTTPException(status_code=404, detail='Company not found')
    check_admin = await inv_crud.get_status_admin(company_id=company_id, user_id=user.id)
    if get_company.owner_id == user.id:
        return user_result.get_user_pass(get_users=get_users)
    if get_company.owner_id != user.id and not check_admin:
        raise HTTPException(status_code=403, detail='You are not the owner or admin')
    return user_result.get_user_pass(get_users=get_users)


# Get user rating
@router.get('/user_rating/{user_id}', response_model=schemas.Rating)
async def get_user_main_rating(user_id: int = Path(..., gt=0)) -> schemas.Rating:
    user = await crud.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    get_users = await analytic_crud.get_user_rating(user_id=user_id)
    res = user_result.get_user_pass(get_users=get_users)
    if res:
        return res[0]
    else:
        raise HTTPException(status_code=404, detail='The user does not have a rating yet')


# Get user's rating for each quiz
@router.get('/list_rating/{user_id}', response_model=List[schemas.ListOfUserResults])
async def list_of_user_rating(user: schemas.UserBaseSchema = Depends(get_current_user)) -> List[
    schemas.ListOfUserResults]:
    return await analytic_crud.get_user_rating(user_id=user.id)


#Gat list of quizzes and user's last time pass quiz
@router.get('/quizzes/last_time', status_code=200)
async def quiz_last_time(user: schemas.UserBaseSchema = Depends(get_current_user)) -> schemas.ListOfUsersResults:
    get_user = await analytic_crud.get_user_rating(user_id=user.id)
    return user_result.get_quiz_last(get_users=get_user)
