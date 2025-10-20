from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, get_password_hash, verify_password
from app.core.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from app.database.database import SessionDep
from app.crud import get_user_by_username
from app.schemas import UserCreate, Token
from app.database.models import User
from app.crud import create_user

router = APIRouter(prefix='/auth', tags=['Auth'])

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
    access_token = create_access_token(
        data={'sub': user.id}
        )
    return Token(access_token=access_token, token_type='bearer')

@router.post('/register', response_model=Token, status_code=status.HTTP_201_CREATED)
async def register_user(user_reg: UserCreate, session: SessionDep):
    exciting_user = await get_user_by_username(session, user_reg.username)
    if exciting_user: 
        raise UserAlreadyExistsError()
    
    user_reg.password = get_password_hash(user_reg.password)
    new_user = await create_user(session, user_reg)
    
    access_token = create_access_token(
        data={'sub': new_user.id}
        )
    return Token(access_token=access_token, token_type='bearer')
