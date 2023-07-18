
# Test_Webtronics

## Tech Stack

**Backend:** FastAPI

**Frontend:** Jinja2, Pure JS

**Server:** Gunicorn

**Services:** Docker, PostgreSQL, Redis


## Run Locally

Clone the project

```bash
  git clone -b vlad https://github.com/vladgenyuk/Tets_WebTronics 
```
```bash
  cd Tets_WebTronics 
```
```bash
  docker-compose up -d
```
http://127.0.0.1:8000/docs 

http://127.0.0.1:8000/pages/personal_area 


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

- Used in Docker, to run without containers - set `localhost`  

`DB_HOST`

`REDIS_HOST`

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



