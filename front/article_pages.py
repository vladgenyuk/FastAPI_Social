import httpx

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from src.jwt_utils.jwt_handler import decode_jwt


router = APIRouter()

templates = Jinja2Templates(directory='front/templates')


@router.get('/articles/{page}')
async def get_articles_front(
        request: Request,
        page: int = 1
):
    token = request.session.get('access_token')
    try:
        email = decode_jwt(token).get('email')
    except:
        return RedirectResponse(url='http://127.0.0.1:8000/pages/personal_area')

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=f'http://127.0.0.1:8000/articles/?page={page}&page_size=5',
        )

    context = {
        'request': request,
        'articles': response.json().get('result'),
        'email': email
    }

    async with httpx.AsyncClient() as client:
        votes = await client.post(
            'http://127.0.0.1:8000/votes/posts_likes_dislikes/',
            json=[i.get('id') for i in context.get('articles')]
        )
    context['votes'] = votes.json()

    # Pagination
    page_info = response.json()
    page_info['result'] = None
    page = page_info.get('page')
    total = page_info.get('total')
    page_size = page_info.get('page_size')
    skip = (page - 1) * page_size
    prev_page = page - 1 if skip > 0 else None
    next_page = page + 1 if skip + page_size < total else None
    context['prev_page'] = prev_page
    context['next_page'] = next_page
    return templates.TemplateResponse('articles.html', context)


@router.get('/create_article')
async def create_article_front(
        request: Request,
):
    token = request.session.get('access_token')
    try:
        email = decode_jwt(token).get('email')
    except:
        return RedirectResponse(url='http://127.0.0.1:8000/pages/personal_area')

    context = {
        'request': request,
        'access_token': token,
        'email': email
    }
    return templates.TemplateResponse('create_article.html', context)


@router.get('/my_articles')
async def get_my_articles_front(
        request: Request
):
    token = request.session.get('access_token')
    try:
        email = decode_jwt(token).get('email')
    except:
        return RedirectResponse(url='http://127.0.0.1:8000/pages/personal_area')

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=f'http://127.0.0.1:8000/articles/my_articles',
            headers={
                'Authorization': f"Bearer {token}"
            },
            params={'email': email}
        )

    if response.status_code != 200:
        return RedirectResponse(url='http://127.0.0.1:8000/pages/personal_area')

    context = {
        'request': request,
        'articles': response.json().get('result'),
        'access_token': token
    }

    async with httpx.AsyncClient() as client:
        votes = await client.post(
            'http://127.0.0.1:8000/votes/posts_likes_dislikes/',
            json=[i.get('id') for i in context.get('articles')]
        )

    context['votes'] = votes.json()
    return templates.TemplateResponse('my_articles.html', context)


@router.get('/update_article/{article_id}')
async def update_article_front(
        request: Request,
        article_id: int
):
    token = request.session.get('access_token')
    try:
        email = decode_jwt(token).get('email')
    except:
        return RedirectResponse(url='http://127.0.0.1:8000/pages/personal_area')

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=f'http://127.0.0.1:8000/articles/{article_id}',
            headers={
                'Authorization': f"Bearer {token}"
            }
        )

    context = {
        'request': request,
        'article': response.json(),
        'email': email,
        'access_token': token
    }
    return templates.TemplateResponse('update_article.html', context)
