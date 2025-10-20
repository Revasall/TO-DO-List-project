from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from app.endpoints import auth_router, user_router, task_router
from app.database.database import lifespan
from app.core.exceptions import *

app = FastAPI(
    title="ToDo List API",
    description="Asynchronous API for managing users and tasks",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(task_router.router)


@app.get('/')
async def root():
    return {'message':'Welcoome to the To-Do API app'}

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code= exc.status_code,
        content={'detail': exc.detail}
    )
