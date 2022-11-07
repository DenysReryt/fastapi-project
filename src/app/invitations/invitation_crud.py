from src.app.database import database
from src.app.models import companies, user_companies, users, invitations_from_users, invitations_from_company
from src.app import schemas
import datetime


from src.app.schemas import Invitation


class InvitationCrud():

    async def get_user_by_id(self, id: int) -> Invitation:
        query = invitations_from_users.select().where(id == invitations_from_users.c.user_id)
        return await database.fetch_one(query=query)

    async def create_inv_to_company(self, user: int, company: int):
        query = invitations_from_users.insert().values(user_id=user, company_id=company)
        return await database.execute(query=query)

    async def users_inv(self, company_id) -> Invitation:
        query = invitations_from_users.select().where(company_id == invitations_from_users.c.company_id)
        return await database.fetch_all(query=query)

    async def ac_rej_user(self, company_id: int, user_id: int, user: schemas.UpdateInvitations) -> Invitation:
        query = invitations_from_users.update().where(user_id == invitations_from_users.c.user_id and company_id ==invitations_from_users.c.company_id).values(
            status=user.status).returning(invitations_from_users.c.user_id)
        await database.execute(query=query)



inv_crud = InvitationCrud()
