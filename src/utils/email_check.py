import requests

from fastapi import HTTPException

from src.config import EMAIL_CHECK_API_KEY


async def validate_email(email: str):
    url = f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={EMAIL_CHECK_API_KEY}'
    response = requests.get(url)
    data = response.json()

    if "@gmail.com" not in email:
        raise HTTPException(
            status_code=400,
            detail='Please enter a valid Gmail'
        )

    if 200 <= response.status_code <= 300 and data['data']['status'] == 'valid':
        return None

    raise HTTPException(
        status_code=400,
        detail='This Gmail address does not exist'
    )
