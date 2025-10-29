from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime      

from app.database.models import User, Task
from app.schemas.schemas import TaskCreate, UserCreate
from app.core.exceptions import ObjectNotFoundError, InvalidDataError, UserNotFoundError
# from app.security.security import get_password_hash


# --- Task CRUD  ---
async def create_task(db: AsyncSession, task_data: TaskCreate, user_id: int) -> Task:
    if not task_data.title:
        raise InvalidDataError('Task title cannot be empty.')
    new_task = Task(
        **task_data.model_dump(),
        owner_id = user_id)
    
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

async def get_list_tasks_titles(db: AsyncSession, 
                                user_id: int, 
                                offset:int, 
                                limit:int,
                                sort_by: str, 
                                status_filter: bool | None = None,
                                priority_filter: int | None = None,
                                sort_order: str = 'asc'
                                ) -> list[dict]:
    
    if not hasattr(Task, sort_by):
        raise ValueError(f"Invalid sort field: {sort_by}")
    
    query = select(Task.id, Task.title, Task.deadline, Task.done).where(Task.owner_id==user_id)
    
    if status_filter is not None:
        query = query.where(Task.done == status_filter)
    if priority_filter is not None:
        query = query.where(Task.priority == priority_filter)

    if sort_order == 'desc':
        query = query.order_by(getattr(Task, sort_by).desc())
    else: 
        query = query.order_by(getattr(Task, sort_by).asc())

    query = query.offset(offset).limit(limit)
    

    tasks = await db.execute(query) 
    
    return [dict(task._mapping) for task in tasks]

async def get_one_task(db: AsyncSession, task_id:int) -> Task:
    task = await db.scalar(select(Task).where(Task.id==task_id))
    if not task:
        raise ObjectNotFoundError('Task')
    return task

async def update_task(db: AsyncSession, task_id: int, data: dict) -> Task:
    task = await db.scalar(select(Task).where(Task.id==task_id))

    if not task:
        raise ObjectNotFoundError('Task')
    
    if not data:
        raise InvalidDataError('Update data cannot be empty.')
    
    for key, value in data.items():
        if value:
            setattr(task, key, value)
            if key == 'done':
                task.completed_at = datetime.now()


    await db.commit()
    await db.refresh(task)
    return task

async def delete_task(db:AsyncSession, task_id: int) -> bool:
    result = await db.execute(delete(Task).where(Task.id==task_id))
    await db.commit()
    return result.rowcount > 0


# --- User CRUD ---

async def create_user(db:AsyncSession, user_data: UserCreate) -> User:
    new_user = User(username=user_data.username, email = user_data.email, hashed_password = user_data.password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user_by_id(db: AsyncSession, user_id:int) -> User:
    user = await db.scalar(select(User).where(User.id==user_id))
    if not user:
        raise UserNotFoundError()
    return user

async def get_user_by_username(db: AsyncSession, username: str) -> User:
    user = await db.scalar(select(User).where(User.username==username))
    return user

async def update_user(db: AsyncSession, user_id: int, data: dict) -> User:
    user = await db.scalar(select(User).where(User.id==user_id))

    if not user:
        raise UserNotFoundError()
    
    if not data:
        raise InvalidDataError('Update data cannot be empty.')
    
    for key, value in data.items():
        if value:
            setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, user_id: int) -> bool:
    result = await db.execute(delete(User).where(User.id==user_id))
    await db.commit()
    return result
