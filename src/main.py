from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from front.article_pages import router as article_pages_router
from front.user_pages import router as user_pages_router
from src.db.database import async_session_maker
from src import api

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="!secret")
app.mount('/static', StaticFiles(directory='front/static'), name='static')


@app.get('/')
async def hello():
    return {"Hello": "For check front pages, go to http://127.0.0.1:8000/pages/personal_area"}


@app.middleware('http')
async def db_session_middleware(request: Request, call_next):
    request.state.session = async_session_maker()
    response = await call_next(request)
    await request.state.session.close()
    return response


app.include_router(
    api.article_router,
    prefix='/articles',
    tags=['articles']
)

app.include_router(
    user_pages_router,
    prefix='/pages',
    tags=['pages']
)

app.include_router(
    api.oauth_router,
    prefix='/oauth',
    tags=['oauth']
)

app.include_router(
    api.auth_router,
    prefix='/auth',
    tags=['auth']
)

app.include_router(
    api.votes_router,
    prefix='/votes',
    tags=['votes']
)


app.include_router(
    article_pages_router,
    prefix='/pages',
    tags=['pages']
)
