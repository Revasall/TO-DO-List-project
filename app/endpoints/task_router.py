from fastapi import APIRouter, HTTPException, status
from typing import List

from app import crud
from app.schemas import TaskSummary, TaskCreate, TaskRead, TaskUpdate
from app.database.database import SessionDep
from app.core.exceptions import TaskNotFoundError, TaskAccessDeniedError
from app.core.security import UserDep
from app.core.access import verify_task_access

router = APIRouter(prefix='/user/tasks', tags=['Tasks'])

@router.post('/', response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate, 
    current_user: UserDep, 
    session: SessionDep
    ):
    
    return await crud.create_task(session, task_data, current_user.id)

@router.get('/', response_model=List[TaskSummary])
async def get_all_tasks(
    current_user: UserDep, 
    session: SessionDep,
    ):
   
   tasks_list = await crud.get_all_tasks_titles(session, current_user.id)
   return tasks_list

@router.get('/{task_id}', response_model=TaskRead)
async def get_one_task(
    task_id: int, 
    current_user: UserDep, 
    session: SessionDep
    ):
    
    task = await crud.get_one_task(session, task_id)
    await verify_task_access(task, current_user.id)
    return task

@router.put('/{task_id}', response_model=TaskRead)
async def update_task(
    task_id: int, 
    update_data: TaskUpdate, 
    current_user: UserDep,  
    session: SessionDep
    ):
    
    task = await crud.get_one_task(session, task_id)
    await verify_task_access(task, current_user.id)
    updated_task = await crud.update_task(session, task_id, update_data.model_dump()) 
    return updated_task
    
@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int, 
    current_user: UserDep, 
    session: SessionDep
    ):
    
    task = await crud.read_one_task(session, task_id)
    await verify_task_access(task, current_user.id)
    await crud.delete_task(session, task_id)
    
    
