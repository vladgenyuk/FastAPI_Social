
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
  


