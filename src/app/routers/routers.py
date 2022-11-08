from fastapi import APIRouter, HTTPException, Path, status, Depends

from typing import List

from src.app.database import engine, metadata, get_redis
from src.app.user_crud import crud
from src.app.companies.company_crud import company_crud
from src.app.invitations.invitation_crud_for_companies import inv_crud
from src.app.invitations.invitation_crud_for_users import inv_crud2
from src.app.quizzes.quiz_crud import quiz_crud
from src.app.quizzes.take_quiz import res_crud
from src.app import schemas

from src.app.config import settings
from src.app.auth0.utils import create_access_token, get_current_user, set_up, get_email_from_token, auth_request

from datetime import timedelta

metadata.create_all(bind=engine)

router = APIRouter()


# Auth
@router.get("/users/login/me", tags=["auth"])
def get_me(user: schemas.UserBaseSchema = Depends(get_current_user)) -> schemas.UserBaseSchema:
    return user

@router.post("/users/login/", tags=["auth"], status_code=status.HTTP_200_OK)
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

@router.post("/users/register/", tags=["auth"], status_code=status.HTTP_200_OK)
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


# Get all users
@router.get('/users/', tags=['Users'], response_model=List[schemas.ListUsersResponse])
async def get_all_users(skip: int = 0, limit: int = 100) -> List[schemas.ListUsersResponse]:
    return await crud.get_users(skip=skip, limit=limit)


# Get user
@router.get('/users/{id}', tags=['Users'], response_model=schemas.UserResponse)
async def get_user(id: int = Path(..., gt=0)) -> schemas.UserResponse:
    user = await crud.get_user_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


# Create user
@router.post('/users/create', tags=['Users'], response_model=schemas.UserBaseSchema)
async def create_user(user: schemas.SignUpSchema) -> schemas.UserBaseSchema:
    db_user = await crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(user=user)


# Update user
@router.put('/users/update', tags=['Users'], response_model=schemas.UserBaseSchema)
async def update_user(user: schemas.UpdateUserSchema, email: str = Depends(get_email_from_token)) -> schemas.UserBaseSchema:
    if user.email == email:
        return await crud.update_user(user)
    raise HTTPException(status_code=400, detail='No user with this email or no permission to execute')


# Delete user
@router.delete('/users/delete', tags=[f'Users'], status_code=status.HTTP_200_OK)
async def delete_user(user: schemas.DeleteUser, email: str = Depends(get_email_from_token), id: schemas.UserResponse = Depends(get_current_user)) -> HTTPException:
    if user.email == email:
        await crud.delete(email=email, id=id.id)
        raise HTTPException(status_code=200, detail='User has been deleted')
    raise HTTPException(status_code=400, detail='No user was found')


# Get all companies
@router.get('/companies/', tags=['Companies'], response_model=List[schemas.ListCompanies])
async def get_all_companies(skip: int = 0, limit: int = 100) -> List[schemas.ListCompanies]:
    return await company_crud.get_companies(skip=skip, limit=limit)


# Create company
@router.post('/companies/create', tags=['Companies'], response_model=schemas.CompanyBaseSchema)
async def create_company(company: schemas.CompanyMain, owner: schemas.UserBaseSchema = Depends(get_current_user)) -> schemas.CompanyBaseSchema:
    return await company_crud.create_company(company=company, owner=owner.id)


#Update company
@router.put('/companies/update/{company_id}', tags=['Companies'], response_model=schemas.CompanyBaseSchema)
async def update_company(company: schemas.CompanyMain, company_id: int = Path(..., gt=0), user: schemas.UserBaseSchema = Depends(get_current_user)) -> schemas.CompanyBaseSchema:
    get_company = await company_crud.get_company_by_id(company_id)
    if not get_company:
        raise HTTPException(status_code=404, detail='Company not found')
    if get_company.owner_id != user.id:
        raise HTTPException(status_code=403, detail='You are not the owner')
    return await company_crud.update_company(company=company, company_id=company_id, user_id=user.id)


# Delete company
@router.delete('/companies/delete/{company_id}', tags=['Companies'], status_code=status.HTTP_200_OK)
async def delete_company(company_id: int = Path(..., gt=0), user: schemas.UserBaseSchema = Depends(get_current_user)) -> HTTPException:
    get_company = await company_crud.get_company_by_id(company_id)
    if not get_company:
        raise HTTPException(status_code=404, detail='Company not found')
    if get_company.owner_id != user.id:
        raise HTTPException(status_code=403, detail='You are not the owner')
    else:
        await company_crud.delete(company_id)
        raise HTTPException(status_code=200, detail='Company has been deleted')


# Invitation

##Users of company
@router.get('/invitations/users/{company_id}', tags=['Invitations from users'], response_model=List[schemas.UsersOfCompany])
async def get_users(company_id: int = Path(..., gt=0), user: schemas.UserBaseSchema = Depends(get_current_user)) -> List[schemas.UsersOfCompany]:
    get_company = await company_crud.get_company_by_id(company_id)
    if not get_company:
        raise HTTPException(status_code=404, detail='Company not found')
    get_company2 = await company_crud.get_company_by_id(company_id)
    if get_company2.owner_id != user.id:
        raise HTTPException(status_code=403, detail='You are not the owner')
    else:
        return await inv_crud.get_all_users(company=company_id)


@router.put('/invitations/update/{company_id}/{user_id}', tags=['Invitations from users'], response_model=schemas.UsersOfCompany)
async def make_admin(company_id: int = Path(..., gt=0), user_id: int = Path(..., gt=0), user: schemas.UserBaseSchema = Depends(get_current_user)) -> schemas.UsersOfCompany:
    get_company = await inv_crud2.get_current_company(company=company_id)
    if not get_company:
        raise HTTPException(status_code=404, detail='Company not found')
    get_user = await inv_crud.get_user_by_id2(user_id)
    if not get_user:
        raise HTTPException(status_code=400, detail='No user was found')
    get_company2 = await company_crud.get_company_by_id(company_id)
    if get_company2.owner_id != user.id:
        raise HTTPException(status_code=403, detail='You are not the owner')
    else:
        return await inv_crud.admin(company_id=company_id, user_id=user_id)


##Invitations from users
@router.get('/invitations/sent/{company_id}', tags=['Invitations from users'], response_model=List[schemas.ListInvitations])
async def get_inv_from_users(company_id: int = Path(..., gt=0), user: schemas.UserBaseSchema = Depends(get_current_user)) -> List[schemas.ListInvitations]:
    get_company = await company_crud.get_company_by_id(company_id)
    if not get_company:
        raise HTTPException(status_code=404, detail='Company not found')
    get_company2 = await company_crud.get_company_by_id(company_id)
    if get_company2.owner_id != user.id:
        raise HTTPException(status_code=403, detail='You are not the owner')
    else:
        return await inv_crud.users_inv(company_id=company_id)


##Create invitation from company to user
@router.post('/invitations/sent/{company_id}/{user_id}', tags=['Invitations from users'], status_code=status.HTTP_200_OK)
async def sent_to_user(company_id: int = Path(..., gt=0), user_id: int = Path(..., gt=0), user: schemas.UserBaseSchema = Depends(get_current_user)) -> HTTPException:
    get_company = await company_crud.get_company_by_id(company_id)
    if not get_company:
        raise HTTPException(status_code=404, detail='Company not found')
    get_company2 = await company_crud.get_company_by_id(company_id)
    if get_company2.owner_id != user.id:
        raise HTTPException(status_code=403, detail='You are not the owner')
    get_user = await crud.get_user_by_id(user_id)
    if not get_user:
        raise HTTPException(status_code=404, detail='User not found')
    else:
        inv = await inv_crud.create_inv_to_user(user=user_id, company=company_id)
        raise HTTPException(status_code=200, detail='Your application is under review')


##Accept invitations from users
@router.post('/invitations/accept/{company_id}/{user_id}', tags=['Invitations from users'], status_code=status.HTTP_200_OK)
async def accept_user(company_id: int = Path(..., gt=0), user_id: int = Path(..., gt=0), user: schemas.UserBaseSchema = Depends(get_current_user)) -> HTTPException:
    get_company = await company_crud.get_company_by_id(company_id)
    if not get_company:
        raise HTTPException(status_code=404, detail='Company not found')
    get_company2 = await company_crud.get_company_by_id(company_id)
    if get_company2.owner_id != user.id:
        raise HTTPException(status_code=403, detail='You are not the owner')
    get_user = await inv_crud.get_user_by_id(user_id)
    if not get_user:
        raise HTTPException(status_code=400, detail='No user was found')
    else:
        await inv_crud.user_acc(company_id=company_id, user_id=user_id)
        raise HTTPException(status_code=200, detail='Successfully accepted')


##Reject invitations from users
@router.post('/invitations/reject/{company_id}/{user_id}', tags=['Invitations from users'], status_code=status.HTTP_200_OK)
async def reject_user(company_id: int = Path(..., gt=0), user_id: int = Path(..., gt=0), user: schemas.UserBaseSchema = Depends(get_current_user)) -> HTTPException:
    get_company = await company_crud.get_company_by_id(company_id)
    if not get_company:
        raise HTTPException(status_code=404, detail='Company not found')
    get_company2 = await company_crud.get_company_by_id(company_id)
    if get_company2.owner_id != user.id:
        raise HTTPException(status_code=403, detail='You are not the owner')
    get_user = await inv_crud.get_user_by_id(user_id)
    if not get_user:
        raise HTTPException(status_code=400, detail='No user was found')
    else:
        await inv_crud.user_rej(company_id=company_id, user_id=user_id)
        raise HTTPException(status_code=200, detail='Successfully rejected')


##Delete user from company
@router.delete('/invitations/delete/{company_id}/{user_id}', tags=['Invitations from users'], status_code=status.HTTP_200_OK)
async def delete_user(company_id: int = Path(..., gt=0), user_id: int = Path(..., gt=0), user: schemas.UserBaseSchema = Depends(get_current_user)) -> HTTPException:
    get_company = await company_crud.get_company_by_id(company_id)
    if not get_company:
        raise HTTPException(status_code=404, detail='Company not found')
    get_company2 = await company_crud.get_company_by_id(company_id)
    if get_company2.owner_id != user.id:
        raise HTTPException(status_code=403, detail='You are not the owner')
    get_user = await inv_crud.get_user_by_id2(user_id)
    if not get_user:
        raise HTTPException(status_code=400, detail='No user was found')
    else:
        await inv_crud.delete_user_from_company(company_id=company_id, user_id=user_id)
        raise HTTPException(status_code=200, detail='Successfully deleted')


##Create invitation from user to company
@router.post('/invitations/sent/{company_id}', tags=['Invitations from companies'], status_code=status.HTTP_200_OK)
async def sent_to_company(company_id: int = Path(..., gt=0), user: schemas.UserBaseSchema = Depends(get_current_user)) -> HTTPException:
    get_company = await company_crud.get_company_by_id(company_id)
    if not get_company:
        raise HTTPException(status_code=404, detail='Company not found')
    if user.id == get_company.owner_id:
        raise HTTPException(status_code=400, detail='You are the owner of this company!')
    else:
        inv = await inv_crud2.create_inv_to_company(user=user.id, company=company_id)
        raise HTTPException(status_code=200, detail='Your application is under review')


##Reject invitations from companies
@router.post('/invitations/reject/{company_id}', tags=['Invitations from companies'], status_code=status.HTTP_200_OK)
async def reject_company(company_id: int = Path(..., gt=0), user: schemas.UserBaseSchema = Depends(get_current_user)) -> HTTPException:
    get_company = await company_crud.get_company_by_id(company_id)
    if not get_company:
        raise HTTPException(status_code=404, detail='Company not found')
    get_inv = await inv_crud2.get_inv_from_company(company_id=company_id, user_id=user.id)
    if not get_inv:
        raise HTTPException(status_code=400, detail='No invitations')
    else:
        await inv_crud2.company_rej(company_id=company_id, user_id=user.id)
        raise HTTPException(status_code=200, detail='Successfully rejected')


##Accept invitations from companies
@router.post('/invitations/accept/{company_id}', tags=['Invitations from companies'], status_code=status.HTTP_200_OK)
async def accept_company(company_id: int = Path(..., gt=0), user: schemas.UserBaseSchema = Depends(get_current_user)) -> HTTPException:
    get_company = await company_crud.get_company_by_id(company_id)
    if not get_company:
        raise HTTPException(status_code=404, detail='Company not found')
    get_inv = await inv_crud2.get_inv_from_company(company_id=company_id, user_id=user.id)
    if not get_inv:
        raise HTTPException(status_code=400, detail='No invitations')
    else:
        await inv_crud2.company_acc(company_id=company_id, user_id=user.id)
        raise HTTPException(status_code=200, detail='Successfully accepted')


# Quizzes
##Get all quizzes
@router.get('/quizzes/', tags=['Quizzes'], response_model=List[schemas.ListQuizzes])
async def get_all_quizzes(skip: int = 0, limit: int = 100) -> schemas.BaseQuiz:
    return await quiz_crud.get_quizzes(skip=skip, limit=limit)


##Create quiz
@router.post('/quizzes/create/{company_id}', tags=['Quizzes'], response_model=schemas.BaseQuiz)
async def create_quiz(quiz: schemas.CreateQuiz, company_id: int = Path(..., gt=0), user: schemas.UserBaseSchema = Depends(get_current_user)) -> schemas.BaseQuiz:
    get_company = await company_crud.get_company_by_id(company_id)
    if not get_company:
        raise HTTPException(status_code=404, detail='Company not found')
    check_admin = await inv_crud.get_status_admin(company_id=company_id, user_id=user.id)
    if not check_admin:
        raise HTTPException(status_code=403, detail='You are not the owner or admin')
    else:
        return await quiz_crud.post_quiz(quiz=quiz, company=company_id)


##Create question
@router.post('/quizzes/create_question/{quiz_id}', tags=['Quizzes'], response_model=schemas.BaseQuestion)
async def create_question(question: schemas.CreateQuestion, quiz_id: int = Path(..., gt=0),
                          user: schemas.UserBaseSchema = Depends(get_current_user)) -> schemas.BaseQuestion:
    quiz = await quiz_crud.check_quiz(quiz_id=quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail='No quiz was found!')
    else:
        get_current_company = await quiz_crud.get_company_by_quiz_id(quiz_id)
        check_admin = await inv_crud.get_status_admin(company_id=get_current_company.company_id, user_id=user.id)
        if not check_admin:
            raise HTTPException(status_code=403, detail='You are not the owner or admin')
        if len(question.answers) < 3:
            raise HTTPException(status_code=404, detail='Min 2 question')
        else:
            return await quiz_crud.post_question(question=question, quiz_id=quiz_id)


##Update quiz
@router.put('/quizzes/update_quiz/{quiz_id}', tags=['Quizzes'], response_model=schemas.BaseQuiz)
async def update_quiz(quiz: schemas.CreateQuiz, quiz_id: int = Path(..., gt=0), user: schemas.UserBaseSchema = Depends(get_current_user)) -> schemas.BaseQuiz:
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
@router.delete('/quizzes/delete_quiz/{quiz_id}', tags=['Quizzes'], status_code=200)
async def delete_quiz(quiz_id: int = Path(..., gt=0), user: schemas.UserBaseSchema = Depends(get_current_user)):
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


# Result
##Get questions by quiz_id
@router.get('/questions/{quiz_id}', tags=['Take a quiz'], response_model=List[schemas.ListQuestion])
async def get_all_questions(quiz_id: int = Path(..., gt=0)) -> schemas.BaseQuestion:
    quiz_get = await quiz_crud.check_quiz(quiz_id=quiz_id)
    if not quiz_get:
        raise HTTPException(status_code=404, detail='No quiz was found!')
    return await res_crud.get_questions(quiz_id=quiz_id)


# ##Take quiz
# @router.put()


@router.get('/set/{key}/{value}/')
async def test(key: str, value: str, redis=Depends(get_redis)):
    redis.set(key, value)
    return
