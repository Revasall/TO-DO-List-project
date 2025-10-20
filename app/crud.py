from sqlalchemy import select, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime      

from app.database.models import User, Task
from app.schemas import TaskCreate, UserCreate


# --- Task CRUD  ---
async def create_task(db: AsyncSession, task_data: TaskCreate, user_id: int) -> Task:
    new_task = Task(
        **task_data.model_dump(),
        owner_id = user_id)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

async def get_all_tasks_titles(db: AsyncSession, user_id: int) -> list[Task]:
    tasks = await db.execute(select(Task.id, Task.title, Task.deadline).where(Task.owner_id==user_id).order_by(Task.priority))
    return [dict(task._mapping) for task in tasks]

async def get_one_task(db: AsyncSession, task_id:int) -> Task:
    task = await db.scalar(select(Task).where(Task.id==task_id))
    return task

async def update_task(db: AsyncSession, task_id: int, data: dict) -> Task:
    task = await db.scalar(select(Task).where(Task.id==task_id))

    if not task:
        return None
    
    if not data:
        return task
    
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
    exciting_user = await db.scalar(select(User).where(or_(User.username==user_data.username, User.email==user_data.email)))
    if exciting_user: 
        raise ValueError("User already exists") #UserExicst
    
    new_user = User(username=user_data.username, email = user_data.email, hashed_password = user_data.password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user_by_id(db: AsyncSession, user_id:int) -> User:
        user = await db.scalar(select(User).where(User.id==user_id))
        return user

async def get_user_by_username(db: AsyncSession, username: str) -> User:
    user = await db.scalar(select(User).where(User.username==username))
    return user

async def update_user(db: AsyncSession, user_id: int, data: dict) -> User:
    user = await db.scalar(select(User).where(User.id==user_id))

    if not user:
        raise ValueError #User not found 
    
    if not data:
        return user
    
    for key, value in data.items():
        if value:
            setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, user_id: int) -> bool:
    result = await db.execute(delete(User).where(User.id==user_id))
    if not result:
        raise ValueError #User not found 
    await db.commit()
    return result






















# # --- User registration
# #....

# # --- Show tasks requests ---
# async def get_tasks(db: AsyncSession, owner_id:int) -> list[Task]:   
#     result = await db.execute(select(Task).where(Task.owner_id==owner_id))
#     return result.scalasrs().all()

# async def get_one_task(db: AsyncSession, task_id:int) -> Task:   
#     result = await db.scalar(select(Task).where(Task.id==task_id))
#     return result


# # # -Filters-
# # async def get_tasks_by_status(db: Session, done: bool) -> list[Task]:
# #     async with async_session() as session:  
# #         await db.scalars(select(Task).where(Task.done == done)).all()
    

# # async def get_tasks_by_deadline(db: Session, date_from:datetime, date_to:datetime):
# #     async with async_session() as session:  
# #         await db.scalars(select(Task).where(
# #             Task.deadline != None,
# #             Task.deadline >= date_from,
# #             Task.deadline <= date_to
# #             )).all()

# # async def get_tasks_by_priority(db: Session, priority: int) -> list[Task]:
# #     async with async_session() as session:
# #         await db.scalars(select(Task).where(Task.priority == priority))
                    

# # --- Create task request---
# async def create_task(db:AsyncSession, task_data: TaskCreate, owner_id: int) -> Task:
#     new_task = Task(
#         **task_data.model_dump(),
#         created_at=datetime.now(),
#         done=False,
#         completed_at=None,
#         owner_id=owner_id
#         )
#     db.add(new_task)
#     db.commit()
#     db.refresh(new_task)
#     await new_task

# # --- Update task requests ---
# async def update_task(db: AsyncSession, task_data: TaskUpdate, task_id: int) -> Task|None:
#     task = select(Task).where(Task.id == task_id)
#     db.commit()
#     db.refresh(task)
#     await task
#     await  None

# async def mark_task_as_done(db: Session, task_id: int) -> Task|None:
#     task = db.scalar(select(Task).where(Task.id == task_id))
#     if task:
#         task.done = True
#         task.completed_at = datetime.now()
#         db.commit()
#         db.refresh(task)
#         return task
#     return None

# # --- Delete task request ---
# async def delete_task(db: Session, task_id: int) -> Task|None:
#     task = db.scalar(select(Task).where(Task.id == task_id))
#     if task:
#         db.delete(task)
#         db.commit()
#         return task
#     return None


