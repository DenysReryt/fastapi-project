from fastapi import APIRouter, HTTPException, Path, Depends

from typing import List

from src.app.database import engine, metadata

from src.app.companies.company_crud import company_crud
from src.app.invitations.invitation_crud_for_companies import inv_crud
from src.app.quizzes.quiz_crud import quiz_crud

from src.app import schemas

from src.app.auth0.utils import get_current_user

metadata.create_all(bind=engine)

router = APIRouter()


# Quizzes
##Get all quizzes
@router.get('/quizzes/', response_model=List[schemas.ListQuizzes])
async def get_all_quizzes(skip: int = 0, limit: int = 100) -> schemas.BaseQuiz:
    return await quiz_crud.get_quizzes(skip=skip, limit=limit)


##Create quiz
@router.post('/create/{company_id}', response_model=schemas.BaseQuiz)
async def create_quiz(quiz: schemas.CreateQuiz, company_id: int = Path(..., gt=0),
                      user: schemas.UserBaseSchema = Depends(get_current_user)) -> schemas.BaseQuiz:
    get_company = await company_crud.get_company_by_id(company_id)
    if not get_company:
        raise HTTPException(status_code=404, detail='Company not found')
    check_admin = await inv_crud.get_status_admin(company_id=company_id, user_id=user.id)
    if get_company.owner_id == user.id:
        return await quiz_crud.post_quiz(quiz=quiz, company=company_id)
    if not check_admin:
        raise HTTPException(status_code=403, detail='You are not the owner or admin')
    else:
        return await quiz_crud.post_quiz(quiz=quiz, company=company_id)


##Create question
@router.post('/create_question/{quiz_id}', response_model=schemas.BaseQuestion)
async def create_question(question: schemas.CreateQuestion, answer: str, quiz_id: int = Path(..., gt=0),
                          user: schemas.UserBaseSchema = Depends(get_current_user)) -> schemas.BaseQuestion:
    quiz = await quiz_crud.check_quiz(quiz_id=quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail='No quiz was found!')
    else:
        get_current_company = await quiz_crud.get_company_by_quiz_id(quiz_id)
        check_admin = await inv_crud.get_status_admin(company_id=get_current_company.company_id, user_id=user.id)
        get_company = await company_crud.get_company_by_id(get_current_company.company_id)
        if get_company.owner_id == user.id:
            return await quiz_crud.post_question(question=question, quiz_id=quiz_id, answer=answer)
        if not check_admin:
            raise HTTPException(status_code=403, detail='You are not the owner or admin')
        else:
            return await quiz_crud.post_question(question=question, quiz_id=quiz_id, answer=answer)


##Update quiz
@router.put('/update_quiz/{quiz_id}', response_model=schemas.BaseQuiz)
async def update_quiz(quiz: schemas.CreateQuiz, quiz_id: int = Path(..., gt=0),
                      user: schemas.UserBaseSchema = Depends(get_current_user)) -> schemas.BaseQuiz:
    quiz_get = await quiz_crud.check_quiz(quiz_id=quiz_id)
    if not quiz_get:
        raise HTTPException(status_code=404, detail='No quiz was found!')
    else:
        get_current_company = await quiz_crud.get_company_by_quiz_id(quiz_id)
        check_admin = await inv_crud.get_status_admin(company_id=get_current_company.company_id, user_id=user.id)
        if not check_admin:
            raise HTTPException(status_code=403, detail='You are not the owner or admin')
        else:
            return await quiz_crud.put_quiz(quiz=quiz, quiz_id=quiz_id, company_id=get_current_company.company_id)


##Delete Quiz
@router.delete('/delete_quiz/{quiz_id}', status_code=200)
async def delete_quiz(quiz_id: int = Path(..., gt=0),
                      user: schemas.UserBaseSchema = Depends(get_current_user)) -> HTTPException:
    quiz_get = await quiz_crud.check_quiz(quiz_id=quiz_id)
    if not quiz_get:
        raise HTTPException(status_code=404, detail='No quiz was found!')
    else:
        get_current_company = await quiz_crud.get_company_by_quiz_id(quiz_id)
        check_admin = await inv_crud.get_status_admin(company_id=get_current_company.company_id, user_id=user.id)
        if not check_admin:
            raise HTTPException(status_code=403, detail='You are not the owner or admin')
        else:
            await quiz_crud.delete(quiz_id=quiz_id)
            raise HTTPException(status_code=200, detail='Successfully deleted')
