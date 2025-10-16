from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()

class UserBase(BaseModel):
    username: str

class User(UserBase):
    password:str

class UserInDB(UserBase):
    hashed_password: str

    
USER_DATA = [
    User(**{'username':'mat', 'password':'123zxc456vbn'}),
    User(**{'username':'mil', 'password':'123456789'})
]

def get_user_from_db(username:str) -> User | None:
    for user in USER_DATA:
        if user.username == username:
            return user
    return None

def authenticate_user(credentials: HTTPBasicCredentials =  Depends(security)) -> User:
    user: User|None = get_user_from_db(credentials.username)
    if user is None or user.password != credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='ivanlid auth')
    else:
        return user
    
@app.get('/login/')
def protected_endpoint(user: User = Depends(authenticate_user)): 
    return {'message': 'You got my secret, welcome'}
