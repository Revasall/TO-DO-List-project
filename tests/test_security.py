import pytest
import jwt
from datetime import timedelta

from app.database.models import User
from app.core.config import settings
from app.core.exceptions import InvalidTokenTypeError, ExpiredTokenError, InvalidTokenError, InvalidCredentialsError
from app.security.security import (get_password_hash, 
                                   verify_password, create_jwt, 
                                   create_access_token, 
                                   create_refresh_token,
                                   decode_jwt_token,
                                   get_current_user)



def test_passport_hash_an_verify():
    password = 'secret'
    hashed = get_password_hash(password)
    
    #Test hashing password
    assert hashed != password
    assert len(hashed) > 20

    #Test verify password
    assert verify_password(password, hashed) is True
    assert verify_password('wrong_pass', hashed) is False


def test_create_jwt_token():
    payload = {'sub': '123', 'type': 'access'}
    token = create_jwt(payload=payload, expires_delta=timedelta(minutes=5))
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert decoded['sub'] == '123'
    assert decoded['type'] == 'access'
    assert 'exp' in decoded

def test_create_access_and_refresh_tokens():
    user = User(id=1, username='john', email='john@example.com')
    access = create_access_token(user)
    refresh = create_refresh_token(user)

    d_access = jwt.decode(access, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    d_refresh = jwt.decode(refresh, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert d_access['type'] == 'access'
    assert d_refresh['type'] == 'refresh'
    assert d_access['sub'] == '1'


def test_decode_jwt_token():

    #Valid token
    payload = {'sub': '1', 'type': 'access'}
    token = create_jwt(payload, timedelta(minutes=5))
    decoded = decode_jwt_token(token, expected_type='access')

    assert decoded['sub'] == '1'

    #Invalid token
    payload = {'sub': '1', 'type': 'refresh'}
    token = create_jwt(payload, timedelta(minutes=5))
    with pytest.raises(InvalidTokenTypeError):
        decode_jwt_token(token, expected_type='access')

    #Expired token
    payload = {'sub': '1', 'type': 'access'}
    token = create_jwt(payload, timedelta(minutes=-1))
    with pytest.raises(ExpiredTokenError):
        decode_jwt_token(token, expected_type='access')

    #Invalid signature
    payload = {'sub': '1', 'type': 'access'}
    token = jwt.encode(payload=payload, key='wrong_key', algorithm=settings.ALGORITHM)
    with pytest.raises(InvalidTokenError):
        decode_jwt_token(token, expected_type='access')


@pytest.mark.asyncio 
async def test_get_current_user(session):
    username = 'delta'
    email = 'delta@example.com'
    password = 'my_password'
    user = User(
        username = username,
        email = email,
        hashed_password = get_password_hash(password))
    session.add(user)
    await session.commit()
    await session.refresh(user)

    token = create_access_token(user)
    result = await get_current_user(token, session=session)
    assert result.id == user.id and  result.username == user.username

    invalid_token = 'invalid_token'
    with pytest.raises(InvalidTokenError):
        await get_current_user(invalid_token, session=session)
    