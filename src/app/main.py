import aioredis
from src.app.database import database
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.config import settings

from src.app.auth0 import routers as auth0
from src.app.users import routers as users
from src.app.companies import routers as companies
from src.app.invitations import routers as invitations
from src.app.quizzes import routers as quizzes
from src.app.result import routers as result
from src.app.analytics import routers as analytics

import uvicorn

app = FastAPI()

## CORSmiddleware
origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth0.router, tags=['Auth'], prefix='/auth')
app.include_router(users.router, tags=['User'], prefix='/users')
app.include_router(companies.router, tags=['Companies'], prefix='/companies')
app.include_router(invitations.router, tags=['Invitations'], prefix='/invitations')
app.include_router(quizzes.router, tags=['Quizzes'], prefix='/quizzes')
app.include_router(result.router, tags=['Take quiz'], prefix='/take_quiz')
app.include_router(analytics.router, tags=['Analytics'], prefix='/analytics')


@app.get('/')
def root():
    return {'status': 'Working'}


@app.on_event("startup")
async def startup():
    await database.connect()
    app.state.redis = await aioredis.from_url(settings.REDIS_URL)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    await app.state.redis.close()


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
