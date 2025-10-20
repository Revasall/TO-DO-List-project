from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserCreate, UserRead, UserUpdate
from app.database.database import SessionDep
from app import crud

router = APIRouter(prefix='/users', tags=['Users'])



@router.get('/{user_id}', response_model=UserRead)
async def get_user(user_id: int, session: SessionDep): # Аўтэнтыфікацыя 
    user = await crud.get_user_by_id(session, user_id)
    return user

    
@router.put('/{users_id}', response_model=UserRead)
async def update_user(user_id: int, user_data: UserUpdate, session: SessionDep):
    updated_user = await crud.update_user(session, user_id, user_data.__dict__)
    return updated_user

@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: SessionDep):
    await crud.delete_user(session, user_id)