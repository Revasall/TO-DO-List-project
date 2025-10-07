from sqlalchemy import select
from sqlalchemy.orm import Session
from models import Task, async_session
from datetime import datetime      



# --- User registration
#....

# --- Show tasks requests ---
async def get_all_tasks(db: Session) -> list[Task]:  
    async with async_session() as session:  
        await db.scalars(select(Task)).all()

# -Filters-
async def get_tasks_by_status(db: Session, done: bool) -> list[Task]:
    async with async_session() as session:  
        await db.scalars(select(Task).where(Task.done == done)).all()
    

async def get_tasks_by_deadline(db: Session, date_from:datetime, date_to:datetime):
    async with async_session() as session:  
        await db.scalars(select(Task).where(
            Task.deadline != None,
            Task.deadline >= date_from,
            Task.deadline <= date_to
            )).all()

async def get_tasks_by_priority(db: Session, priority: int) -> list[Task]:
    async with async_session() as session:
        await db.scalars(select(Task).where(Task.priority == priority))
                    
async def get_task_by_id(db: Session, task_id: int) -> Task|None:
    async with async_session() as session:
        await db.scalar(select(Task).where(Task.id == task_id))

# --- Create task request---
async def create_task(db:Session, title: str, description:str=None, deadline:datetime=None, priority:int=0) -> Task:
    async with async_session() as session:
        new_task = Task(
            title=title, 
            description=description,
            deadline=deadline,
            priority=priority,
            created_at=datetime.now(),
            done=False,
            completed_at=None
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        await new_task

# --- Update task requests ---
async def update_task(db: Session, 
                      task_id: int, 
                      new_title: str = None, 
                      new_description: str= None,
                      new_deadline: datetime = None, 
                      new_priority: int = None
                      ) -> Task|None:
    
    async with async_session() as session: 
        task = db.scalar(select(Task).where(Task.id == task_id))
        if task:
            if new_title:
                task.title = new_title
            if new_description:
                task.description = new_description
            if new_deadline:
                task.deadline = new_deadline
            if new_priority:
                task.priority = new_priority
            db.commit()
            db.refresh(task)
            await task
        await  None

async def mark_task_as_done(db: Session, task_id: int) -> Task|None:
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task:
        task.done = True
        task.completed_at = datetime.now()
        db.commit()
        db.refresh(task)
        return task
    return None

# --- Delete task request ---
async def delete_task(db: Session, task_id: int) -> Task|None:
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task:
        db.delete(task)
        db.commit()
        return task
    return None


