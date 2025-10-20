from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserCreate, UserRead, UserUpdate
from app.database.database import SessionDep
from app import crud

router = APIRouter(prefix='/users', tags=['Users'])



@router.get('/{user_id}', response_model=UserRead)
async def get_user(user_id: int, session: SessionDep): # Аўтэнтыфікацыя 
    user = await crud.read_user(session, user_id)
    if not user: 
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user

    
@router.put('/{users_id}', response_model=UserRead)
async def update_user(user_id: int, user_data: UserUpdate, session: SessionDep):
    updated_user = await crud.update_user(session, user_id, user_data.__dict__)
    if not updated_user: 
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return updated_user

@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: SessionDep):
    succes = await crud.delete_user(session, user_id)
    if not succes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
