from src.app.database import database
from src.app.models import companies, user_companies, users, invitations_from_users, invitations_from_company, users_of_company
from src.app import schemas
import datetime


from src.app.schemas import Invitation


class InvitationCrud():

    async def get_inv_from_company(self, user_id: int, company_id: int):
        query = invitations_from_company.select().where(user_id == invitations_from_company.c.user_id, company_id == invitations_from_company.c.company_id)
        return await database.execute(query=query)

    async def create_inv_to_company(self, user: int, company: int):
        query = invitations_from_users.insert().values(user_id=user, company_id=company)
        return await database.execute(query=query)

    async def company_acc(self, company_id: int, user_id: int):
        query1 = users_of_company.insert().values(company_id=company_id, user_id=user_id)
        query2 = invitations_from_company.delete().where(user_id == invitations_from_company.c.user_id, company_id == invitations_from_company.c.company_id)
        await database.execute(query=query2)
        return await database.execute(query=query1)

    async def company_rej(self, company_id: int, user_id: int):
        query2 = invitations_from_company.delete().where(user_id == invitations_from_company.c.user_id,
                                                       company_id == invitations_from_company.c.company_id)
        await database.execute(query=query2)





inv_crud2 = InvitationCrud()
