from fastapi import APIRouter, HTTPException, Path, status, Depends

from typing import List

from src.app.database import engine, metadata
from src.app.users.user_crud import crud
from src.app.companies.company_crud import company_crud
from src.app.invitations.invitation_crud_for_companies import inv_crud
from src.app.invitations.invitation_crud_for_users import inv_crud2

from src.app import schemas

from src.app.auth0.utils import get_current_user

metadata.create_all(bind=engine)

router = APIRouter()

# Invitation

##Users of company
@router.get('/users/{company_id}', response_model=List[schemas.UsersOfCompany])
async def get_users(company_id: int = Path(..., gt=0), user: schemas.UserBaseSchema = Depends(get_current_user)) -> List[schemas.UsersOfCompany]:
    get_company = await company_crud.get_company_by_id(company_id)
    if not get_company:
        raise HTTPException(status_code=404, detail='Company not found')
    get_company2 = await company_crud.get_company_by_id(company_id)
    if get_company2.owner_id != user.id:
        raise HTTPException(status_code=403, detail='You are not the owner')
    else:
        return await inv_crud.get_all_users(company=company_id)


@router.put('/update/{company_id}/{user_id}', response_model=schemas.UsersOfCompany)
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
@router.get('/sent/{company_id}', response_model=List[schemas.ListInvitations])
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
@router.post('/sent/{company_id}/{user_id}', status_code=status.HTTP_200_OK)
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
@router.post('/accept/{company_id}/{user_id}', status_code=status.HTTP_200_OK)
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
@router.post('/reject/{company_id}/{user_id}', status_code=status.HTTP_200_OK)
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
@router.delete('/delete/{company_id}/{user_id}', status_code=status.HTTP_200_OK)
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
@router.post('/sent/{company_id}', status_code=status.HTTP_200_OK)
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
@router.post('/reject/{company_id}', status_code=status.HTTP_200_OK)
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
@router.post('/accept/{company_id}', status_code=status.HTTP_200_OK)
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
