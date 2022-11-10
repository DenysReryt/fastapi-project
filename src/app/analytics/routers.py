import aioredis
from fastapi import APIRouter, HTTPException, Path, Depends

import csv
from typing import List

from src.app.database import engine, metadata
from src.app.quizzes.quiz_crud import quiz_crud
from src.app.analytics.analytic_crud import analytic_crud
from src.app.invitations.invitation_crud_for_companies import inv_crud
from src.app.companies.company_crud import company_crud
from src.app.result.take_quiz import res_crud
from src.app import schemas
from src.app.config import settings

from src.app.result.user_result import make_rating, get_user_result_redis

from src.app.auth0.utils import get_current_user

metadata.create_all(bind=engine)

router = APIRouter()

# Get analytic of user
@router.get('/{user_id}', response_model=List[schemas.ListOfUserResults])
async def get_user(user: schemas.UserResponse = Depends(get_current_user), quiz_id: int, result: float, user_id: int = Path(..., gt=0)):
    # get_company = await analytic_crud.get_company_id(user_id)
    # check_admin = await inv_crud.get_status_admin(company_id=get_company, user_id=user.id)
    # if get_company.owner_id == user.id:
    return await analytic_crud.get_user_results(user_id=user_id)
    # if not check_admin:
    #     raise HTTPException(status_code=403, detail='You are not the owner or admin')
    #
    # get_user = await analytic_crud.get_user_results(user_id=user_id)
    # if not get_user:
    #     raise HTTPException(status_code=400, detail='the user was not found or the user did not pass any quiz')


