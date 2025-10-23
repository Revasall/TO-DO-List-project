import jwt
from fastapi import Depends
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from typing import Annotated

from app.core.config import settings
from app.core.exceptions import ExpiredTokenError, InvalidTokenError, InvalidTokenTypeError, InvalidCredentialsError
from app.database.database import SessionDep
from app.database.models import User
from app.crud import get_user_by_id

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS


password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
http_bearer = HTTPBearer(auto_error=False)

def get_password_hash(password:str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password:str, hashed_password:str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def create_jwt(payload: dict, expires_delta: timedelta):
    to_encode = payload.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({'exp':expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt

def create_access_token(
        user: User, 
        expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES
        ) -> str:
    
    payload = {
        'sub': str(user.id),
        'email': user.email,
        'type': 'access'
        }
    expires_delta = timedelta(minutes=expires_delta)
    
    return create_jwt(payload=payload, expires_delta=expires_delta)

def create_refresh_token(
        user: User, 
        expires_delta: int = REFRESH_TOKEN_EXPIRE_DAYS
        ) -> str:
    
    payload = {
        'sub': str(user.id),
        'type': 'refresh'
        }
    expires_delta = timedelta(days=expires_delta)

    return create_jwt(payload=payload, expires_delta=expires_delta)

def decode_jwt_token(token:str, expected_type: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload['type'] != expected_type:
            raise InvalidTokenTypeError(token_type=payload['type'], 
                                        expected_type=expected_type)
        return payload
    except jwt.ExpiredSignatureError: 
        raise ExpiredTokenError()
    except jwt.InvalidTokenError:
        raise InvalidTokenError()
    
async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: SessionDep
        ):
    
    try:
        payload = decode_jwt_token(token, expected_type='access')
        user_id: str = payload.get('sub')
        if user_id is None:
            raise InvalidCredentialsError
    except jwt.PyJWTError:
        raise InvalidCredentialsError
    
    user = await get_user_by_id(session, int(user_id))
    if user is None:
        raise InvalidCredentialsError
    return user

UserDep = Annotated[User, Depends(get_current_user)]