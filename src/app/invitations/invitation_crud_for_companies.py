from src.app.database import database
from src.app.models import companies, user_companies, users, invitations_from_users, invitations_from_company, users_of_company
from src.app import schemas
import datetime


from src.app.schemas import Invitation


class InvitationCrud():

    async def get_user_by_id(self, id: int) -> Invitation:
        query = invitations_from_users.select().where(id == invitations_from_users.c.user_id)
        return await database.fetch_one(query=query)

    async def get_user_by_id2(self, id: int) -> Invitation:
        query = users_of_company.select().where(id == users_of_company.c.user_id)
        return await database.fetch_one(query=query)

    async def create_inv_to_user(self, user: int, company: int):
        query = invitations_from_company.insert().values(user_id=user, company_id=company)
        return await database.execute(query=query)

    async def users_inv(self, company_id) -> Invitation:
        query = invitations_from_users.select().where(company_id == invitations_from_users.c.company_id)
        return await database.fetch_all(query=query)

    async def user_acc(self, company_id: int, user_id: int):
        query1 = users_of_company.insert().values(company_id=company_id, user_id=user_id)
        query2 = invitations_from_users.delete().where(user_id == invitations_from_users.c.user_id, company_id == invitations_from_users.c.company_id)
        await database.execute(query=query2)
        return await database.execute(query=query1)

    async def user_rej(self, company_id: int, user_id: int):
        query2 = invitations_from_users.delete().where(user_id == invitations_from_users.c.user_id,
                                                       company_id == invitations_from_users.c.company_id)
        await database.execute(query=query2)

    async def delete_user_from_company(self, company_id: int, user_id: int):
        query = users_of_company.delete().where(user_id == users_of_company.c.user_id,
                                                       company_id == users_of_company.c.company_id)
        await database.execute(query=query)





inv_crud = InvitationCrud()
