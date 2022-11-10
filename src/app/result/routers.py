import aioredis
from fastapi import APIRouter, HTTPException, Path, Depends

from typing import List

from src.app.database import engine, metadata
from src.app.quizzes.quiz_crud import quiz_crud
from src.app.result.take_quiz import res_crud
from src.app import schemas
from src.app.config import settings

from src.app.result.user_result import make_rating, get_user_result_redis

from src.app.auth0.utils import get_current_user

metadata.create_all(bind=engine)

router = APIRouter()


# Result
##Get questions by quiz_id
@router.get('/questions/{quiz_id}', tags=['Take a quiz'], response_model=List[schemas.ListQuestion])
async def get_all_questions(quiz_id: int = Path(..., gt=0)) -> schemas.BaseQuestion:
    quiz_get = await quiz_crud.check_quiz(quiz_id=quiz_id)
    if not quiz_get:
        raise HTTPException(status_code=404, detail='No quiz was found!')
    return await res_crud.get_questions(quiz_id=quiz_id)


##Take quiz
@router.post('/quizzes/take_quiz/{quiz_id}/', tags=['Take a quiz'], status_code=200)
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
        redis_key, res_to_save = get_user_result_redis(user_id=user.id, quiz_id=quiz_id, user_answers=answer_input)
        await redis.hset(redis_key, mapping=res_to_save)

        return await res_crud.put_user_result(score=f'{quiz_score}/{len(right_answers)}', result=result, quiz_id=quiz_id,
                                          user_id=user.id, company_id=get_current_company.company_id)



# def get_user_result(user_id: int, quiz_id: int):

# @router.get('/set/{key}/{value}/')
# async def test(key: str, value: str, redis=Depends(get_redis)):
#     redis.set(key, value)
#     return redis.get(key)
