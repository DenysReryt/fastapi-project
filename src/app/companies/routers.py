from fastapi import APIRouter, HTTPException, Path, status, Depends

from typing import List

from src.app.database import engine, metadata
from src.app.companies.company_crud import company_crud

from src.app import schemas

from src.app.auth0.utils import get_current_user

metadata.create_all(bind=engine)

router = APIRouter()


# Get all companies
@router.get('/', response_model=List[schemas.ListCompanies])
async def get_all_companies(skip: int = 0, limit: int = 100) -> List[schemas.ListCompanies]:
    return await company_crud.get_companies(skip=skip, limit=limit)


# Create company
@router.post('/create', response_model=schemas.CompanyBaseSchema)
async def create_company(company: schemas.CompanyMain,
                         owner: schemas.UserBaseSchema = Depends(get_current_user)) -> schemas.CompanyBaseSchema:
    return await company_crud.create_company(company=company, owner=owner.id)


# Update company
@router.put('/update/{company_id}', response_model=schemas.CompanyBaseSchema)
async def update_company(company: schemas.CompanyMain, company_id: int = Path(..., gt=0),
                         user: schemas.UserBaseSchema = Depends(get_current_user)) -> schemas.CompanyBaseSchema:
    get_company = await company_crud.get_company_by_id(company_id)
    if not get_company:
        raise HTTPException(status_code=404, detail='Company not found')
    if get_company.owner_id != user.id:
        raise HTTPException(status_code=403, detail='You are not the owner')
    return await company_crud.update_company(company=company, company_id=company_id, user_id=user.id)


# Delete company
@router.delete('/delete/{company_id}', status_code=status.HTTP_200_OK)
async def delete_company(company_id: int = Path(..., gt=0),
                         user: schemas.UserBaseSchema = Depends(get_current_user)) -> HTTPException:
    get_company = await company_crud.get_company_by_id(company_id)
    if not get_company:
        raise HTTPException(status_code=404, detail='Company not found')
    if get_company.owner_id != user.id:
        raise HTTPException(status_code=403, detail='You are not the owner')
    else:
        await company_crud.delete(company_id)
        raise HTTPException(status_code=200, detail='Company has been deleted')
