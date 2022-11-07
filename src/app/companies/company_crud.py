from src.app.database import database
from src.app.models import companies, user_companies
from src.app import schemas
import datetime


from src.app.schemas import CompanyBaseSchema


class CompanyCrud():

    async def get_companies(self, skip: int = 0, limit: int = 100) -> CompanyBaseSchema:
        query = companies.select().where(companies.c.visibility == True).offset(skip).limit(limit)
        return await database.fetch_all(query=query)

    async def get_company_by_id(self, id: int) -> CompanyBaseSchema:
        query = companies.select().where(id == companies.c.id)
        return await database.fetch_one(query=query)

    async def create_company(self, company: schemas.CompanyMain, owner: int) -> CompanyBaseSchema:

        db_company = companies.insert().values(name=company.name, visibility=company.visibility, description=company.description, owner_id=owner)
        company_id = await database.execute(db_company)
        user_and_companies = user_companies.insert().values(user_id=owner, company_id=company_id)
        await database.execute(user_and_companies)
        return schemas.CompanyBaseSchema(**company.dict(), id=company_id, owner_id=owner, created_at=datetime.datetime.now())

    async def update_company(self, company: schemas.CompanyMain, company_id: int, user_id: int) -> CompanyBaseSchema:
        query = (companies.update().where(company_id == companies.c.id, user_id == companies.c.owner_id).values(
            name=company.name,
            visibility=company.visibility,
            description=company.description).returning(company_id == companies.c.id, user_id == companies.c.owner_id))
        ex = await database.execute(query=query)
        company_get = await database.fetch_one(companies.select().where(company_id == companies.c.id))
        return schemas.CompanyBaseSchema(**company.dict(), id=company_get.id, owner_id=company_get.owner_id, created_at=company_get.created_at)

    async def delete(self, company_id: int) -> CompanyBaseSchema:
        query1 = user_companies.delete().where(company_id == user_companies.c.company_id)
        await database.execute(query=query1)
        query2 = companies.delete().where(company_id == companies.c.id)
        return await database.execute(query=query2)

company_crud = CompanyCrud()
