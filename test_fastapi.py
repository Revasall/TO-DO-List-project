import secrets
from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends, status
import jwt
from pydantic import BaseModel
from fastapi.security import  OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone

SECRET_KEY = 'f7cd7831d9f816b716621dc8650ef568db20ddf06ca69f2301477690b1a539bb'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
password_hash = PasswordHash.recommended()


class UserBase(BaseModel):
    username: str

class User(UserBase):
    password:str

class UserInDB(UserBase):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    
USER_DATA = [
    UserInDB(**{'username':'mat', 'hashed_password':'$argon2id$v=19$m=65536,t=3,p=4$aXTX2Rq7WZ3ymFEpZIs4bg$QKYfe7vVx+RK/MY6IM8snk8p8Ab51TaIaDRbMnxKNUc'}),
    UserInDB(**{'username':'mil', 'hashed_password':'$argon2id$v=19$m=65536,t=3,p=4$RucV2QYfL9oeEcsGa0eJ2g$VUU6TDAv6FNQmQKR5k5pNGlVSQb1pPmQuCQ03vHckms'})
]

def hashing_password(password: str) -> str:
    return password_hash.hash(password)
  
def password_verify(plain_password:str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def get_user_from_db(username:str) -> UserInDB | None:
    for user in USER_DATA:
        if secrets.compare_digest(user.username, username):
            return user
    return None


def create_jwt_token(data: dict, expire_delta: timedelta|None = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def authenticate_user(username: str, password:str) -> User:
    user = get_user_from_db(username)
    if not user:
        return None
    if not password_verify(password, user.hashed_password):
        return None
    return user


@app.post('/login')
async def login(credentials: Annotated[OAuth2PasswordRequestForm, Depends()] ):
    invalid_cred = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail='invalid username or password',
        headers={"WWW-Authenticate": "Bearer"}
        )

    user = authenticate_user(credentials.username, credentials.password)
    if not user:
        raise invalid_cred
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_jwt_token(
        data={'sub': user.username}, expire_delta=access_token_expires
        )
    return Token(access_token=access_token, token_type='Bearer')

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
        )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if not username:
            raise credential_exception
        token_data = TokenData(username=username)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Task has expired',
            headers={"WWW-Authenticate": "Bearer"})
    except:
        raise credential_exception
    
    user = get_user_from_db(token_data.username)
    if not user :
        raise credential_exception
    return user

    


@app.post('/register')
async def registeration_user(user: User):
    try:
        user_in_db = get_user_from_db(user.username)
        if user_in_db:
            raise HTTPException(status_code=409, detail="User already exists")
        USER_DATA.append(UserInDB(username=user.username, 
                              hashed_password=hashing_password(user.password))
                              )
        return {"message": "New user created"}
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=('User registration error'))

@app.get('/protected_resource')
async def protected_endpoint(user: Annotated[UserInDB, Depends(get_current_user)]): 
    return {'message': f'Welcome {user.username}, your user_info: {user}'}
