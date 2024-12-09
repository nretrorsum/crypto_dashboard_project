import uuid
from datetime import timedelta, datetime
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from starlette import status
from database.database_connection import db_dependency
from database.database_models import UserTable
from database.repository import repository
from auth.models import User, Token
from passlib.context import CryptContext
from config import SECRET_KEY, ALGORITHM

auth_router = APIRouter()


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')

async def authenticate_user(email: str, hashed_password: str, db):
    data = await db.execute(
        select(UserTable)
        .where(UserTable.email == email)
    )
    user = data.scalars().first()
    if not user:
        return False
    if not bcrypt_context.verify(hashed_password, user.hashed_password):
        return False

    return user

async def create_access_token(email: str, user_id: uuid.UUID, expiration: timedelta):
    encode = {'sub': email, 'id': str(user_id)}
    expires = datetime.utcnow() + expiration
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def create_refresh_token(email:str, expiration: timedelta):
    encode = {'sub': email}
    expires = datetime.utcnow() + expiration
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        user_id: str = payload.get('id')
        exp: int = payload.get('exp')
        if exp < datetime.utcnow().timestamp():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired')
        if email is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not authenticate user')
        return {'email': email, 'user_id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not authenticate user')

@auth_router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(request: User, db: db_dependency):
    expiration =  timedelta(weeks=4)

    create_user_model =UserTable(
        id = uuid.uuid4(),
        name = request.name,
        email = request.email,
        hashed_password = bcrypt_context.hash(request.hashed_password),
        subscription= request.subscription,
        start_time = datetime.utcnow(),
        end_time = datetime.utcnow() + expiration,
        join_date = datetime.utcnow(),
        is_active = request.is_active,
        is_verified = request.is_verified,
    )

    db.add(create_user_model)
    await db.commit()

    return {'message': 'User created'}

@auth_router.post('/token', response_model=Token)
async def create_auth_tokens(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency, response: Response):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not authenticate user')

    if not await repository.get_refresh_token(user.email):
        refresh_token = await create_refresh_token(user.email, timedelta(weeks=4))
        await repository.add_refresh_token(refresh_token, user.email)
        response.set_cookie(
            key='a576fhe8gfg8egy3v_new',
            value = await repository.get_refresh_token(user.email),
            max_age = 120,
            secure = False,
            httponly=True,
            samesite='lax'
        )

    access_token = await create_access_token(user.email, user.id, timedelta(minutes=60))
    response.set_cookie(
        key='authToken',
        value=access_token,
        max_age= 60,
        secure= False,
        httponly=True,
        samesite='lax'
    )

    response.set_cookie(
        key='a576fhe8gfg8egy3v',
        value= await repository.get_refresh_token(user.email),
        max_age=120,
        secure=False,
        httponly=True,
        samesite='lax'
    )

    return {'access_token': access_token, 'token_type': 'Bearer', 'user_id': user.id}

user_dependency = Annotated[dict, Depends(get_current_user)]

