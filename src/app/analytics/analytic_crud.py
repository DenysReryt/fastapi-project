from src.app.schemas import ListOfUserResults, UserResponse
from src.app.models import rating, companies
from src.app import schemas
from src.app.database import database


class AnalyticCrud():
    async def get_company_id(self, user_id):
        query = companies.select().where(user_id == companies.c.owner_id)
        return await database.fetch_all(query=query)


    async def get_user_results(self, user_id: int) -> ListOfUserResults:
        query = rating.select().where(user_id == rating.c.user_id)
        return await database.fetch_all(query=query)


analytic_crud = AnalyticCrud()
