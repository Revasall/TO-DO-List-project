import pytest
from sqlalchemy import select

from app.database.models import User
from app.security.security import get_password_hash, decode_jwt_token
from app.core.config import settings


@pytest.mark.asyncio
async def test_register_user(client, session):
    payload = {
        'username': 'john',
        'email': 'jonhdoe@example.com',
        'password':'secret_pass'
    }

    responce = await client.post('/auth/register', json=payload)
    assert responce.status_code in (200, 201)
    data = responce.json()
    assert 'access_token' in data and 'refresh_token' in data and data['token_type'] == 'bearer'

    result = await session.execute(select(User).where(User.username==payload['username']))
    user = result.scalar_one_or_none()
    assert user is not None
    assert user.id == int(decode_jwt_token(data['access_token'], 'access')['sub'])
    assert user.email == payload['email']
    assert user.hashed_password != payload['password']
    assert len(user.hashed_password) > 20

@pytest.mark.asyncio
async def test_login_and_get_current_user(client, test_user, auth_header):

    #Get test_user from test DB
    username = test_user.username
    password = 'password'

    #Login
    responce = await client.post(
        '/auth/login',
        data = {'username':username, 'password': password}
        )
    assert responce.status_code == 200
    data = responce.json()
    assert 'access_token' in data and 'refresh_token' in data
    access = data['access_token']

    #decode access token 
    payload = decode_jwt_token(access, expected_type='access')
    assert str(payload.get('sub')) == str(test_user.id)

    #request to protected endpoint /auth/me
    me_responce = await client.get('/users/me', headers=auth_header)
    assert me_responce.status_code == 200
    me_data = me_responce.json()
    assert me_data['username'] == username

@pytest.mark.asyncio
async def test_refresh_token(client, test_user):

    #Get test_user from test DB
    username = test_user.username
    password = 'password'

    responce = await client.post(
        '/auth/login',
        data = {'username':username, 'password': password}
        )
    assert responce.status_code == 200
    data = responce.json()
    assert 'access_token' in data and 'refresh_token' in data
    refresh = data['refresh_token']

    #Using refresh for get new access and refresh tokens
    ref_responce = await client.post('/auth/refresh', headers={"Authorization": f"Bearer {refresh}"})
    assert ref_responce.status_code == 200
    ref_data = ref_responce.json()
    assert 'access_token' in ref_data and 'refresh_token' in ref_data
    new_access = ref_data['access_token']
    new_refresh = ref_data['refresh_token']

    #Token validity check
    access_payload = decode_jwt_token(new_access, expected_type='access')
    refresh_payload = decode_jwt_token(new_refresh, expected_type='refresh')
    assert str(access_payload.get('sub')) == str(test_user.id) and str(access_payload.get('sub')) == str(test_user.id)

    