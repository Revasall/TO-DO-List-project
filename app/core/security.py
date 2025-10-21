import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from typing import Annotated

from app.core.config import settings
from app.core.exceptions import ExpiredTokenError, InvalidTokenError, InvalidCredentialsError
from app.database.database import SessionDep
from app.database.models import User
from app.crud import get_user_by_id

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

def get_password_hash(password:str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password:str, hashed_password:str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({'exp':expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def decode_acces_token(token:str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
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
        payload = decode_acces_token(token)
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