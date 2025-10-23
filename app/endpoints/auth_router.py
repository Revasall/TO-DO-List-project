from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, create_refresh_token, decode_jwt_token, get_password_hash, verify_password
from app.core.exceptions import InvalidCredentialsError, UserAlreadyExistsError, ExpiredTokenError
from app.database.database import SessionDep
from app.crud import get_user_by_id, get_user_by_username
from app.schemas import UserCreate, Token
from app.database.models import User
from app.crud import create_user

router = APIRouter(prefix='/auth', tags=['Auth'])
http_bearer = HTTPBearer()

async def autenticate_user(db: AsyncSession, username: str, plain_password: str) -> User | None :
    user = await get_user_by_username(db, username)
    if not user or not verify_password(plain_password, user.hashed_password):
        return None
    return user

@router.post('/login')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep) -> Token:
    user = await autenticate_user(session, form_data.username, form_data.password)
    if not user: 
        raise InvalidCredentialsError()
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
        )

@router.post('/refresh')
async def refresh_token(
    session: SessionDep,
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):

    payload = decode_jwt_token(credentials.credentials, expected_type='refresh')
    user_id: str = payload['sub']
    if user_id is None:
        raise InvalidTokenError()
    
    user = await get_user_by_id(db=session, user_id=int(user_id))
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )



@router.post('/register', response_model=Token, status_code=status.HTTP_201_CREATED)
async def register_user(user_reg: UserCreate, session: SessionDep):
    exciting_user = await get_user_by_username(session, user_reg.username)
    if exciting_user: 
        raise UserAlreadyExistsError()
    
    user_reg.password = get_password_hash(user_reg.password)
    new_user = await create_user(session, user_reg)
    
    access_token = create_access_token(user=new_user)
    refresh_token = create_refresh_token(user=new_user)

    return Token(
        access_token=access_token, 
        refresh_token=refresh_token)
