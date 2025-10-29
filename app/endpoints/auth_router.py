from typing import Annotated
from fastapi import APIRouter, Depends, Request, status
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.security.limiter import limiter
from app.security.security import create_access_token, create_refresh_token, decode_jwt_token, get_password_hash, verify_password
from app.core.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from app.database.database import SessionDep
from app.crud.crud import get_user_by_id, get_user_by_username, create_user
from app.schemas.schemas import UserCreate, Token
from app.database.models import User

router = APIRouter(prefix='/auth', tags=['Auth'])
http_bearer = HTTPBearer()

async def autenticate_user(db: AsyncSession, username: str, plain_password: str) -> User | None :
    
    user = await get_user_by_username(db, username)
    if not user or not verify_password(plain_password, user.hashed_password):
        return None
    return user

@router.post('/login')
@limiter.limit('10/minute')
async def login(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
    ) -> Token:

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
@limiter.limit('10/10minute')
async def refresh_token(
    request: Request,
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
@limiter.limit('1/minute')
async def register_user(
    request: Request,
    user_reg: UserCreate, 
    session: SessionDep
    ):
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
