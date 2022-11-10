from src.app.schemas import ListOfUserResults, ListOfUsersResults
from src.app.models import rating, companies
from src.app import schemas
from src.app.database import database


class AnalyticCrud():
    async def get_company_id(self, user_id) -> schemas.CompanyBaseSchema:
        query = companies.select().where(user_id == companies.c.owner_id)
        return await database.fetch_all(query=query)

    async def get_user_results(self, user_id: int, company_id: int) -> ListOfUserResults:
        query = rating.select().where(user_id == rating.c.user_id, company_id == rating.c.company_id)
        return await database.fetch_all(query=query)

    async def get_users_results(self, company_id: int) -> ListOfUsersResults:
        query = rating.select().where(company_id == rating.c.company_id)
        return await database.fetch_all(query=query)

    async def get_user_rating(self, user_id: int) -> schemas.Rating:
        query = rating.select().where(user_id == rating.c.user_id)
        return await database.fetch_all(query=query)

    async def get_user_rating(self, user_id: int) -> schemas.Rating:
        query = rating.select().where(user_id == rating.c.user_id)
        return await database.fetch_all(query=query)

analytic_crud = AnalyticCrud()
