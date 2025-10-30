# To-Do List Api

This project is a REST API for managing a list of tasks (to-do list), developed using FastAPI.
The main goal of the project is to demonstrate the implementation of secure authentication through JWT tokens, working with PostgreSQL through SQLAlchemy, as well as the use of pytest for unit testing and rate limiting to protect against excessive requests.

The API supports user registration and authorization, CRUD operations for tasks, token updates, and implements a clear layered architecture (app/core, app/database, app/routers, app/schemas).

![To-Do List API icon](https://github.com/Revasall/TO-DO-List-project/blob/main/media_readme/71edf952-2431-452b-9d76-49633047c48f.png?raw=true)

## Project structure
```
app/
├── core/
│   ├── config.py
│   └── exceptions.py
├── crud/
│   └── crud.py
├── database/
│   ├── models.py
│   ├── database.py
├── endpoints/
│   ├── auth_router.py
│   ├── tasks_router.py
│   └── users_router.py
├── schemas/
│   └── schemas.py
└── security/
    └── security.py

main.py
.env
.gitignore
```
## Features

- __User registration and user login endpoints (with jwt tokens)__
  - Implemented in the app/endpoints/auth_router file, where a json request with the entered username and password is required for user registration. The password is hashed using the pwdlib library.
  - User login is implemented using oauth2, after which access and refresh jwt tokens are issued.
  - Here, verification and decryption of the access token is also implemented to obtain user data from the database and its access to the action in the system.

- __CRUD operations for managing the to-do list__
  - Implemented in the app/endpoints/task_router, app/endpoints/user_router and app/crud/crud files, in which the protected endpoints access the database.
  - For the user, the operations get, update and delete are available.
  - For tasks, the operations create, get_one_task, which calls the task by its id, get_tasks_list with implemented sorting, filtering and pagination, as well as update and delete are available.

- __Asynchronous work with DB through SQLAlchemy__
  - Asynchronous engines and sessions for working with the PostgreSQL database
  - Interaction with the database is implemented through SQLAlchemy

- __Rate limiting to protect the API__
  - Implemented request throttling for registration, login, and refresh token endpoints using the slowapi library

- __Tests using Pytest (fixtures, mock sessions, fake DB)__
  - Implemented integration and unit tests using pytest
  - A fake SQLite database is used for the tests using an asynchronous approach

## Technologies

- Python 3.12.6
- FastAPI
- SQLAlchemy 2.0, Alembic
- PostgreSQL + asyncpg
- JWT authentication, Argon2 (password hash)
- SlowAPI

Other libraries and technologies used can be found in requirements.txt.

## Installation and launch
Downloading the project:

```git clone https://github.com/Revasall/TO-DO-List-project.git```

```cd TO-DO-List-project```

Setting up the environment:
```python -m venv .venv```

```
source .venv/bin/activate      # for Linux/macOS
.venv\Scripts\activate   # for Windows
source .venv/Scripts/activate # for bush
```

```pip install -r requirements.txt```

Create a database in PostgreSQL
Configure the .env file as in .env.example

Launching Alembic and running the project:

```alembic upgrade head```

```uvicorn app.main:app --reload```


The API will now be accessible at http://127.0.0.1:8000
Swagger documentation: http://127.0.0.1:8000/docs

## Testing

To test against tests, use in command line:
```pytest -v```

To test in a browser, use the following queries:

registration:
```
curl POST http://127.0.0.1:8000/auth/register

{
  "username": "string",
  "email": "user@example.com",
  "password": "string"
}
```
login:

```
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test_user&password=mysecretpassword"
```
refresh:

```
curl -X POST "http://127.0.0.1:8000/auth/refresh" \
  -H "Authorization: Bearer <refresh_token>"
```

get user info:
```
curl -X 'GET' \
  'http://127.0.0.1:8000/users/me' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer {access_token}
```

create task:
```
curl -X POST "http://127.0.0.1:8000/user/tasks/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
  "title": "string",
  "description": "string",
  "deadline": "2025-10-30T11:46:25.569Z",
  "priority": 0
  }'
```

get task
```
curl -X GET "http://127.0.0.1:8000/user/tasks/1" \
  -H "Authorization: Bearer <access_token>"
```

You can test the remaining endpoints on http://127.0.0.1:8000/docs


## Author 

Macvej Reut 

Python backend developer

Philosopher and logician

📧 Email: [matvejreut@gmail.com]

🐙 GitHub: [https://github.com/Revasall]
