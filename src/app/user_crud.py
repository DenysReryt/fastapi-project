from src.app.database import database
from src.app.models import users
from src.app import schemas


class UserCrud():

    async def get_users(skip: int = 0, limit: int = 100):
        query = users.select().offset(skip).limit(limit)
        return await database.fetch_all(query=query)

    async def create_user(user: schemas.SignUpSchema):
        db_user = users.insert().values(first_name=user.first_name, last_name=user.last_name, email=user.email,
                                        password=user.password, role=user.role, verified=user.verified)
        user_id = await database.execute(db_user)
        return {**user.dict(), 'id': user_id}

    async def get_user_by_email(email: str):
        return await database.fetch_one(users.select().where(users.c.email == email))

    async def get_user_by_id(id: int):
        query = users.select().where(id == users.c.id)
        return await database.fetch_one(query=query)

    async def update_user(id: int, user: schemas.UpdateUserSchema):
        query = (users.update().where(id == users.c.id).values(
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role)
            .returning(users.c.id))
        return await database.execute(query=query)

    async def delete(id: int):
        query = users.delete().where(id == users.c.id)
        return await database.execute(query=query)

