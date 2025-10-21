from app.core.exceptions import TaskNotFoundError, TaskAccessDeniedError
from app.database.models import Task

async def verify_task_access(task: Task | None, user_id: int) -> Task:
    if not task:
        raise TaskNotFoundError
    if task.owner_id != user_id:
        raise TaskAccessDeniedError
    return task