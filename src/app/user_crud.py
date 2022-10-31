from src.app.database import database
from src.app.models import users
from src.app import schemas
import datetime
import secrets

from src.app.schemas import UserBaseSchema


class UserCrud():

    async def create_user_by_email(self, email: str) -> UserBaseSchema:
        db_user = users.insert().values(first_name='first_name', last_name="last_name", email=email,
                                        password=str(secrets.token_hex(10)), role='user', verified=False)
        user = await database.execute(db_user)
        return schemas.UserBaseSchema(id=user, email=email, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())

    async def get_users(self, skip: int = 0, limit: int = 100) -> UserBaseSchema:
        query = users.select().offset(skip).limit(limit)
        return await database.fetch_all(query=query)

    async def create_user(self, user: schemas.SignUpSchema) -> UserBaseSchema:
        db_user = users.insert().values(first_name=user.first_name, last_name=user.last_name, email=user.email,
                                        password=user.password, role=user.role, verified=user.verified)
        user_id = await database.execute(db_user)
        return schemas.UserBaseSchema(**user.dict(), id=user_id, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())

    async def get_user_by_email(self, email: str) -> UserBaseSchema:
        user = await database.fetch_one(users.select().where(users.c.email == email))
        if user is None:
            return None
        return user

    async def get_user_by_id(self, id: int) -> UserBaseSchema:
        query = users.select().where(id == users.c.id)
        return await database.fetch_one(query=query)

    async def update_user(self, user: schemas.UpdateUserSchema) -> UserBaseSchema:
        query = (users.update().where(user.email == users.c.email).values(
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
            password=user.password,
            updated_at=datetime.datetime.now())
            .returning(users.c.email))
        user_id = await database.execute(query=query)
        user_get_id = await database.fetch_one(users.select().where(user.email == users.c.email))
        return schemas.UserBaseSchema(**user.dict(), id=user_get_id.id, created_at=user_get_id.created_at, updated_at=user_get_id.updated_at)

    async def delete(self, email: str) -> None:
        query = users.delete().where(email == users.c.email)
        return await database.execute(query=query)

crud = UserCrud()
