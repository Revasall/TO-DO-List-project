from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import TaskSummary, TaskCreate, TaskRead, TaskUpdate
from app.database.database import get_session
from app import crud

router = APIRouter(prefix='/user/tasks', tags=['Tasks'])
SessionDep = Annotated[AsyncSession, Depends(get_session)]

@router.post('/{user_id}', response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(task_data: TaskCreate, user_id: int, session: SessionDep):
    try: 
        return await crud.create_task(session, task_data, user_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
@router.get('/{user_id}', response_model=List[TaskSummary])
async def get_all_tasks(user_id:int, session: SessionDep):
   tasks_list = await crud.read_all_tasks_titles(session, user_id)
   return tasks_list

@router.get('/task/{task_id}', response_model=TaskRead)
async def read_one_task(task_id: int, session: SessionDep):
    task = await crud.read_one_task(session, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    return task

@router.put('/task/{task_id}', response_model=TaskRead)
async def update_task(task_id: int, update_data: TaskUpdate, session: SessionDep):
    updated_task = await crud.update_task(session, task_id, update_data.model_dump()) 
    if not updated_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    return updated_task
    
@router.delete('/task/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, session: SessionDep):
    success = await crud.delete_task(session, task_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    return 
    
