from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.schemas import UserCreate, UserRead, UserUpdate
from app.database.database import SessionDep
from app.core.security import UserDep


router = APIRouter(prefix='/users', tags=['Users'])



@router.get('/me', response_model=UserRead)
async def get_user(current_user: UserDep): 
    return current_user

    
@router.put('/me', response_model=UserRead)
async def update_user(
    current_user: UserDep, 
    user_data: UserUpdate, 
    session: SessionDep):
    updated_user = await crud.update_user(
        session, 
        current_user.id, 
        user_data.__dict__)
    return updated_user

@router.delete('/me', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(current_user: UserDep, session: SessionDep):
    await crud.delete_user(session, current_user.id)