import pytest
from sqlalchemy import select

from app.database.models import User
from app.security.security import create_access_token, verify_password
import copy

@pytest.mark.asyncio 
async def test_get_user(client, test_user, auth_header):
    responce = await client.get('/users/me', headers=auth_header)
    assert responce.status_code == 200
    data = responce.json()
    assert data['username'] == test_user.username
    
@pytest.mark.asyncio
async def test_update_user(client, test_user, auth_header, session):
    payload = {
        'username':'update_test_user',
        'email':'update_email@example.com',
        'password':'update_password'
    }
    responce = await client.put('/users/me', headers=auth_header, json = payload)
    assert responce.status_code == 200
    data = responce.json()
    assert data['username'] == payload['username']
    assert data['email'] == payload['email']

    user_from_db = await session.execute(select(User).where(User.id == test_user.id))
    user_data = user_from_db.scalar_one_or_none() 

    assert user_data.username == payload['username']
    assert user_data.email == payload['email']
    assert verify_password(payload['password'], user_data.hashed_password)

@pytest.mark.asyncio
async def test_delete_user(client, session):
    user = User(
        username = 'test_user',
        email = 'test_user@example.com',
        hashed_password ='password'
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    token = create_access_token(user)

    responce = await client.delete('/users/me', 
                                   headers={'Authorization': f'Bearer {token}'})
    
    assert responce.status_code == 204
    del_user = await session.scalar(select(User).where(User.id == user.id))
    assert del_user is None
