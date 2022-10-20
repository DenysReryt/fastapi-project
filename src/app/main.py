from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.config import settings
from src.app.routers import crud_user
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

app.include_router(crud_user.router, tags=['Users'], prefix='/users')


@app.get('/')
def root():
    return {'status': 'Working'}


# @app.on_event("startup")
# async def startup():
#     await database.connect()
#     app.state.redis = await aioredis.from_url(REDIS_URL)
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()
#     await app.state.redis.close()


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
