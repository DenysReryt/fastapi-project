import aioredis
from fastapi import APIRouter, HTTPException, Path, Depends
from fastapi.responses import FileResponse

from typing import List

from src.app.database import engine, metadata
from src.app.quizzes.quiz_crud import quiz_crud
from src.app.result.take_quiz import res_crud
from src.app import schemas
from src.app.config import settings

from src.app.result.user_result import make_rating
from src.app.companies.company_crud import company_crud
from src.app.invitations.invitation_crud_for_companies import inv_crud
from src.app.auth0.utils import get_current_user

metadata.create_all(bind=engine)

router = APIRouter()


# Result
##Get questions by quiz_id
@router.get('/questions/{quiz_id}', response_model=List[schemas.ListQuestion])
async def get_all_questions(quiz_id: int = Path(..., gt=0)) -> schemas.BaseQuestion:
    quiz_get = await quiz_crud.check_quiz(quiz_id=quiz_id)
    if not quiz_get:
        raise HTTPException(status_code=404, detail='No quiz was found!')
    return await res_crud.get_questions(quiz_id=quiz_id)


##Take quiz
@router.post('/{quiz_id}/', status_code=200)
async def pass_quiz(answer_input: List[schemas.AnswerInput], quiz_id: int = Path(..., gt=0),
                    user: schemas.UserBaseSchema = Depends(get_current_user)) -> HTTPException:
    quiz_get = await quiz_crud.check_quiz(quiz_id=quiz_id)
    if not quiz_get:
        raise HTTPException(status_code=404, detail='No quiz was found!')
    get_current_company = await quiz_crud.get_company_by_quiz_id(quiz_id)
    right_answers = await res_crud.get_right_answers(quiz_id=quiz_id)
    quiz_score, right_answers, result = make_rating(answer_input=answer_input, right_answers=right_answers)
    if quiz_score == 's':
        raise HTTPException(status_code=400, detail='To pass the quiz you need to answer all the questions')
    else:
        redis = await aioredis.from_url(settings.REDIS_URL)
        redis_key = f'user:{user.id}_company:{get_current_company.company_id}_quiz:{quiz_id}'
        await redis.set(redis_key, result)

        return await res_crud.put_user_result(score=f'{quiz_score}/{len(right_answers)}', result=result,
                                              quiz_id=quiz_id,
                                              user_id=user.id, company_id=get_current_company.company_id)


# Get csvfile of company's one user result
@router.post('/download_result/user/company/{company_id}/{user_id}', status_code=200)
async def download_company_one_user_result(user_id: int = Path(..., gt=0), company_id: int = Path(..., gt=0), user: schemas.UserBaseSchema = Depends(get_current_user)) -> FileResponse:
    get_company = await company_crud.get_company_by_id(company_id)
    if_user = await res_crud.if_user_in_company(user_id=user_id, company_id=company_id)
    if not if_user:
        raise HTTPException(status_code=404, detail='There is no such user in the company')
    if not get_company:
        raise HTTPException(status_code=404, detail='Company not found')
    check_admin = await inv_crud.get_status_admin(company_id=company_id, user_id=user.id)
    if get_company.owner_id != user.id:
        if not check_admin:
            raise HTTPException(status_code=403, detail='You are not the owner or admin')
        else:
            await res_crud.one_user_of_company(user_id=user_id, company_id=company_id)
            return FileResponse('export_company_user_results.csv')
    else:
        await res_crud.one_user_of_company(user_id=user_id, company_id=company_id)
        return FileResponse('export_company_user_results.csv')


# Get csvfile of company's users result
@router.post('/download_result/users/company/{company_id}', status_code=200)
async def download_company_users_result(company_id: int = Path(..., gt=0), user: schemas.UserBaseSchema = Depends(get_current_user)) -> FileResponse:
    get_company = await company_crud.get_company_by_id(company_id)
    if not get_company:
        raise HTTPException(status_code=404, detail='Company not found')
    check_admin = await inv_crud.get_status_admin(company_id=company_id, user_id=user.id)
    if get_company.owner_id != user.id:
        if not check_admin:
            raise HTTPException(status_code=403, detail='You are not the owner or admin')
        else:
            await res_crud.all_users_results(company_id=company_id)
            return FileResponse('export_company_results.csv')
    else:
        await res_crud.all_users_results_csv(company_id=company_id)
        return FileResponse('export_company_results.csv')


# Get csvfile of user result
@router.post('/download_result/my', status_code=200)
async def download_user_result(user: schemas.UserBaseSchema = Depends(get_current_user)) -> FileResponse:
    await res_crud.user_results_csv(user_id=user.id)
    return FileResponse('export_user_results.csv')
