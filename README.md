
# Tech Stack

**Backend:** FastAPI

**Frontend:** Jinja2, Pure JS

**Server:** Gunicorn

**Services:** Docker, PostgreSQL, Redis


# Run Locally with docker-compose


```bash
  git clone -b vlad https://github.com/vladgenyuk/Tets_WebTronics 
```
```bash
  cd Tets_WebTronics 
```
```bash
  docker-compose up -d
```

# Run Locally without docker-compose


```bash
  git clone -b vlad https://github.com/vladgenyuk/Tets_WebTronics 
```
```bash
  docker run --name webtronics_db -d -p 5432:5432 -e POSTGRES_USER=vlad -e POSTGRES_PASSWORD=qseawdzxc1 postgres

  docker run --name redis_cache -d -p 6379:6379 redis  
```
- Set .env `DB_HOST`, `REDIS_HOST` as `localhost`

```bash
  uvicorn src.main:app --reload
```


# Environment Variables

To run this project, you will need to add the following environment variables to your .env file

- Secret password that used to register users via OAuth

`OAUTH_SECRET_PASSWORD`

- Secret code to encode JWT token

`JWT_SECRET`

- My Google and Github OAuth credentials (fake)

`GIT_CLIENT_ID`

`GOOGLE_CLIENT_ID`

`GIT_SECRET`

`GOOGLE_SECRET`

- Email Hunter API KEY

`EMAIL_CHECK_API_KEY`

### OAuth origins
- Google
  Authorized JS origins
    - http://127.0.0.1:8000
    - http://localhost:8000

  Authorized redirect url
    - http://127.0.0.1:8000/oauth/auth/google
    - http://localhost:8000/oauth/auth/google
- Github
  Homepage URL
  - http://127.0.0.1:8000/personal_area

  Authorization callback URL
  - http://127.0.0.1:8000/oauth/auth/github


## Registration and Authorization

I made 2 types of authorization for users: using email and password, Oauth2 from Github and Google

Model User contains `oauth` and `account_id` options that are credentials of Google and Github accounts. 

Sometimes Github profiles are without email, i decided to set `base{id}@{provider}.com` as email that also an unique identifier for other endpoints

#### JWT

JWT tokens are generated by endpoints `signup`, `login` and stored at *Session Middleware* 

`current_user` endpoint is used to decode token, stored at *session* dictionary and return token 
`logout` endpoint need to be requested to delete access_token and logout user respectively

#### OAuth2

`oauth/auth/google`, `oauth/auth/github` endpoints are used to get read-only information from google and github accounts and register users in DB via `OAUTH_SECRET_PASSWORD` by requesting other endpoints with this informatin
  

## Pagination

`articles` GET endpoint has a pagination, I implemented it at database level, base_crud class has method *get_paginated* that makes a query to database with offset and limit parameters, base *page_size* = 5. I don't used any 3-rd party libraries for pagination.

## Votes Redis 

I implemented likes and dislikes with Redis as a cache storage, user makes request to `toggle_like_dislike` endpoint to leave his vote, it prevents Like cheating, and both like-dislikes votes by 4 if-else structure.

`posts_likes_dislikes` endpoint is used to get information about likes and dislikes of each article to display it on front

Information about votes is only stored in redis, it guarantees consistensy of information and fast responses from this endpoints via in-memory storage

## Frontend

I used build-in in FastAPI Jinja2 template generator and pure JS to display information on web pages and add active behaviour on pages. Endpoints with pages run on the same host and port as the main application

To imitate the suspended Frontend application, the endpoints and HTML templates makes additional requests to backend

