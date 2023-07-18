import time

import httpx

from datetime import datetime, timedelta
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from authlib.integrations.starlette_client import OAuth, OAuthError

from src.config import GIT_SECRET, GOOGLE_SECRET, GOOGLE_CLIENT_ID, GIT_CLIENT_ID, OAUTH_SECRET_PASSWORD


router = APIRouter()

oauth = OAuth()

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
SIGNUP_URL = 'http://127.0.0.1:8000/auth/signup'
LOGIN_URL = 'http://127.0.0.1:8000/auth/login'


oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_SECRET,
    # instead of server_metadata_url ________________________________
    # access_token_url="https://accounts.google.com/o/oauth2/token",
    # authorize_url="https://accounts.google.com/o/oauth2/auth",
    # api_base_url="https://www.googleapis.com/oauth2/v1/",
    # jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

oauth.register(
    name='github',
    client_id=GIT_CLIENT_ID,
    client_secret=GIT_SECRET,
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize",
    jwks_uri='https://jwt.io/',
    client_kwargs={"scope": "user:email"},
)


@router.get('/login/google')
async def login_google(request: Request):
    redirect_uri = request.url_for('auth_google')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get('/auth/google')
async def auth_google(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')

    user = token.get('userinfo')

    user_register = {
        "username": user.get('name'),
        "email": user.get('email') or "base" + str(user.get('sub')) + '@google.com',
        "password": OAUTH_SECRET_PASSWORD,
        "repeat_password": OAUTH_SECRET_PASSWORD,

        "oauth": "google",
        "account_id": str(user.get('sub'))
    }

    user_get = {
        'email': user_register.get('email'),
        'password': user_register.get('password')
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            LOGIN_URL,
            json=user_get,
        )

    async with httpx.AsyncClient() as client:
        reg_response = await client.post(
            url=SIGNUP_URL,
            json=user_register
        )

    redirect = RedirectResponse(url='http://127.0.0.1:8000/pages/personal_area')

    if reg_response.status_code == 403:
        redirect.set_cookie(
            key='info',
            value="User with this email already exists, please log in with password",
            expires=(datetime.utcnow() + timedelta(seconds=1)).strftime("%a, %d %b %Y %H:%M:%S GMT"))

    request.session['access_token'] = response.json().get('access_token') or reg_response.json().get('access_token')

    return redirect


@router.get('/login/github')
async def login_github(request: Request):
    redirect_uri = request.url_for('auth_github')
    return await oauth.github.authorize_redirect(request, redirect_uri)


@router.get('/auth/github')
async def auth_github(request: Request):
    try:
        token = await oauth.github.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')

    access_token = token.get('access_token')

    headers = {
        'client_id': GIT_CLIENT_ID,
        'client_secret': GIT_SECRET,
        # 'code': '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',
        'Authorization': f'Bearer {access_token}'
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            'https://api.github.com/user',
            headers=headers
        )  # fetching data from GitHub api

    user = response.json()

    user_register = {
        "username": user.get('login'),
        "email": user.get('email') or "base" + str(user.get('id')) + '@github.com',
        "password": OAUTH_SECRET_PASSWORD,
        "repeat_password": OAUTH_SECRET_PASSWORD,

        "oauth": "github",
        "account_id": str(user.get('id'))
    }

    user_get = {
        'email': user_register.get('email'),
        'password': user_register.get('password')
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            LOGIN_URL,
            json=user_get,
        )

    async with httpx.AsyncClient() as client:
        reg_response = await client.post(
            url=SIGNUP_URL,
            json=user_register
        )

    redirect = RedirectResponse(url='http://127.0.0.1:8000/pages/personal_area')

    if reg_response.status_code == 403:
        redirect.set_cookie(
            key='info',
            value="User with this email already exists, please log in with password",
            expires=(datetime.utcnow() + timedelta(seconds=1)).strftime("%a, %d %b %Y %H:%M:%S GMT"))

    request.session['access_token'] = response.json().get('access_token') or reg_response.json().get('access_token')

    return redirect
