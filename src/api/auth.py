from fastapi import APIRouter, Body, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from starlette.responses import RedirectResponse

from src.jwt_utils.jwt_handler import sign_jwt, decode_jwt
from src.schemas.user import UserCreate, UserLogin, Token
from src.utils.email_check import validate_email
from src import crud


router = APIRouter()


@router.post('/signup')
async def user_signup(
        request: Request,
        user: UserCreate = Body(default=None)
):
    if user.oauth == 'vlad':
        await validate_email(user.email)

    session: AsyncSession = request.state.session
    result = await crud.user.create_user(session, user.dict())

    token = sign_jwt(user.email)
    request.session['access_token'] = token.get('access_token')
    return token


@router.post('/login')
async def user_login(
        request: Request,
        user: UserLogin = Body()
):
    session: AsyncSession = request.state.session
    check_user = await crud.user.get_registered_user(
        session,
        user.email,
        user.password
    )
    if not check_user:
        raise HTTPException(status_code=401, detail="Wrong email or password")
    token = sign_jwt(user.email)
    request.session['access_token'] = token.get('access_token')
    return token


@router.post('/current_user')
async def current_user(request: Request, token_body: Token = None):
    if token_body:
        token = decode_jwt(token_body.access_token)
    else:
        token = request.session.get('access_token')
        token = decode_jwt(token)
    if not token:
        raise HTTPException(status_code=401, detail='Not Authorized')
    return token


@router.get('/logout')
async def logout(request: Request):
    request.session.pop('access_token', None)
    return RedirectResponse(url='http://127.0.0.1:8000/pages/personal_area')
