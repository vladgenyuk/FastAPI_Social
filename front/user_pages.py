import httpx
from fastapi import APIRouter, Request
from front.article_pages import templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.user import User


router = APIRouter()


@router.get('/register')
async def register_user_front(
        request: Request,
):
    context = {
        'request': request
    }
    return templates.TemplateResponse('register.html', context)


@router.get('/personal_area')
async def sign_in_page(request: Request):
    token = request.session.get('access_token')
    if token:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url='http://127.0.0.1:8000/auth/current_user',
                json={'access_token': token}
            )
    else:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url='http://127.0.0.1:8000/auth/current_user',
            )

    info = request.cookies.get('info')

    if response.status_code == 401:  # 200, 401 Not authenticated
        return templates.TemplateResponse('auth.html', {
            "request": request,
            'info': info or ""
        })

    session: AsyncSession = request.state.session
    stmt = select(User).where(User.email == response.json().get('email'))
    user = (await session.execute(stmt)).scalar_one_or_none()
    if not user:
        return templates.TemplateResponse('auth.html', {
            "request": request,
            'info': info or ""
        })

    context = {
        'request': request,
        'user': user,
    }

    return templates.TemplateResponse('personal_area.html', context)
