from src.app.database import database
from src.app.models import companies, user_companies
from src.app import schemas
import datetime


from src.app.schemas import CompanyBaseSchema


class CompanyCrud():

    async def get_company_by_id(self, id: int) -> CompanyBaseSchema:
        query = companies.select().where(id == companies.c.id)
        return await database.fetch_one(query=query)

    async def create_company(self, company: schemas.MainCompany, owner: int) -> CompanyBaseSchema:

        db_company = companies.insert().values(name=company.name, visibility=company.visibility, description=company.description, owner_id=owner)
        company_id = await database.execute(db_company)
        user_and_companies = user_companies.insert().values(user_id=owner, company_id=company_id)
        await database.execute(user_and_companies)
        return schemas.CompanyBaseSchema(**company.dict(), id=company_id, owner_id=owner, created_at=datetime.datetime.now())

    async def update_company(self, company: schemas.MainCompany, company_id: int, user_id: int) -> CompanyBaseSchema:
        query = (companies.update().where(company_id == companies.c.id and user_id == companies.c.owner_id).values(
            name=company.name,
            visibility=company.visibility,
            description=company.description).returning(company_id == companies.c.id and user_id == companies.c.owner_id))
        ex = await database.execute(query=query)
        company_get = await database.fetch_one(companies.select().where(company_id == companies.c.id))
        return schemas.CompanyBaseSchema(**company.dict(), id=company_get.id, owner_id=company_get.owner_id, created_at=company_get.created_at)


company_crud = CompanyCrud()
