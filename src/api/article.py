import math, httpx

from sqlalchemy.ext.asyncio.session import AsyncSession

from fastapi import APIRouter, Request, Depends, HTTPException, Query

from src import crud
from src.jwt_utils.jwt_handler import decode_jwt
from src.jwt_utils.jwt_bearer import JWTBearer
from src.models.article import Article
from src.schemas.article import ArticleCreate
from src.utils.exceptions import IDNotFoundException

router = APIRouter()


@router.get('/count')
async def get_articles_count(
        request: Request
):
    session: AsyncSession = request.state.session
    result = await crud.article.get_count(session)
    return {'count': result}


@router.get('/my_articles', dependencies=[Depends(JWTBearer())])
async def get_my_articles(
        request: Request,
        email: str
):
    session: AsyncSession = request.state.session
    result = await crud.article.get_my_articles(session, email)

    return {
        'result': result,
    }


@router.get('/')
async def get_articles(
        request: Request,
        page: int = Query(1, ge=1),
        page_size: int = Query(5, ge=1),
):
    session: AsyncSession = request.state.session
    result = await crud.article.get_paginated(session, page, page_size)
    async with httpx.AsyncClient() as client:
        total = await client.get(
            url='http://127.0.0.1:8000/articles/count'
        )
    total = total.json().get('count')

    return {
        'result': result,
        'page': page,
        'total': total,
        'page_size': page_size,
        'pages': math.ceil(total / page_size)
    }


@router.get('/{article_id}')
async def get_article_by_id(
        request: Request,
        article_id: int
):
    session: AsyncSession = request.state.session
    result = await crud.article.get_by_id(session, article_id)
    return result


@router.post('/', dependencies=[Depends(JWTBearer())])
async def create_article(
        request: Request,
        article: ArticleCreate
):
    article_data = article.dict()

    session: AsyncSession = request.state.session
    result = await crud.article.create(session, article_data)
    return result


@router.put('/{article_id}', dependencies=[Depends(JWTBearer())])
async def update_article(
        request: Request,
        new_article: ArticleCreate,
        article_id: int,
):
    session: AsyncSession = request.state.session
    current_article: Article = await crud.article.get_by_id(session, article_id)
    if not current_article:
        raise IDNotFoundException(
            model=Article,
            id=article_id
        )
    token = request.session['access_token']
    user = decode_jwt(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail='You are not authorized'
        )
    if user.get('email') != current_article.author_email:
        raise HTTPException(
            status_code=403,
            detail="You are not the author to update this article"
        )
    article_updated = await crud.article.update_article(
        session=session,
        current_article=current_article,
        new_article=new_article
        )
    return article_updated


@router.delete('/{article_id}', dependencies=[Depends(JWTBearer())])
async def delete_article(
        request: Request,
        article_id: int,
):
    session: AsyncSession = request.state.session
    current_article: Article = await crud.article.get_by_id(session, article_id)
    if not current_article:
        raise IDNotFoundException(
            model=Article,
            id=article_id
        )
    token = request.session['access_token']
    user = decode_jwt(token)

    if not user:
        raise HTTPException(
            status_code=401,
            detail='You are not authorized'
        )

    if user.get('email') != current_article.author_email:
        raise HTTPException(
            status_code=403,
            detail="You are not Authorized or Not the Author to update this article"
        )

    article_delete = await crud.article.delete(
        session=session,
        id=article_id
        )

    return article_delete
