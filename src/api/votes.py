import redis

from fastapi import APIRouter, Query, Depends, Body
from pydantic import constr
from typing import List

from src.config import REDIS_HOST


router = APIRouter()

r = redis.Redis(host=REDIS_HOST, port=6379)


def get_redis():
    return r


votes = constr(regex='^(like|dislike)$')


@router.post("/toggle_like_dislike/{post_id}/{user_email}/{action}")
async def toggle_like_dislike(post_id: int, user_email: str, action: votes, r=Depends(get_redis)):
    if action == "like":
        if r.sismember(f"post:{post_id}:likes", user_email):
            r.srem(f"post:{post_id}:likes", user_email)
            return {"post_id": post_id, "author_email": user_email, "liked": False}
        else:
            r.sadd(f"post:{post_id}:likes", user_email)
            r.srem(f"post:{post_id}:dislikes", user_email)
            return {"post_id": post_id, "author_email": user_email, "liked": True}
    else:
        if r.sismember(f"post:{post_id}:dislikes", user_email):
            r.srem(f"post:{post_id}:dislikes", user_email)
            return {"post_id": post_id, "author_email": user_email, "disliked": False}
        else:
            r.sadd(f"post:{post_id}:dislikes", user_email)
            r.srem(f"post:{post_id}:likes", user_email)
            return {"post_id": post_id, "author_email": user_email, "disliked": True}


@router.post("/posts_likes_dislikes/")
async def get_posts_likes_dislikes(ids: List[int] = Body(...)):
    result = {}
    for post_id in ids:
        likes = r.scard(f"post:{post_id}:likes")
        dislikes = r.scard(f"post:{post_id}:dislikes")
        result[post_id] = {
            "likes": int(likes) if likes else 0,
            "dislikes": int(dislikes) if dislikes else 0,
        }
    return result


@router.post("/user/{user_email}/posts")
async def get_user_posts_likes_dislikes(user_email: str, post_ids: List[int] = Query(...)):
    result = {}
    for post_id in post_ids:
        liked = r.sismember(f"post:{post_id}:likes", user_email)
        disliked = r.sismember(f"post:{post_id}:dislikes", user_email)
        result[post_id] = {"liked": liked, "disliked": disliked}
    return result
