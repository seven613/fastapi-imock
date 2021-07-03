#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :chapter06.py
@说明        :
@时间        :2021/07/03 11:40:58
@作者        :张强
@版本        :1.0
'''

from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pydantic import BaseModel, EmailStr

from passlib.context import CryptContext
from jose import JWTError, jwt

app06 = APIRouter()

"""
OAuth2PasswordBearer是接收URL作为参数的一个类：客户端会向该URL发送username和password，然后得到一个token值
OAuth2PasswordBearer并不会创建相应的URL路径操作，只是指明了客户端用来请求token的URL地址
当请求来到的时候，FastAPI会检查请求中Head中Authorization头信息，如果没有找到Authorization头信息，或者头信息不是Bearer token,它会返回401状态码UNAUTHORIZED
"""
# 获取token
oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/chapter06/token")  # 请求token的url地址


@app06.get('/oauth2_password_bearer')
async def oauth2_password_bearer(token: str = Depends(oauth2_schema)):
    return{'token': token}

""" 基于Password 和Bearer token的OAuth2认证"""
fake_users_db = {
    "john snow": {
        "username": "john snow",
        "full_name": "John Snow",
        "email": "johnsnow@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True
    }
}

# 密码哈希


def fake_hash_password(password: str):
    return "fakehashed"+password

# 用户模型类


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

# 数据库中的用户模型类


class UserInDB(User):
    hashed_password: str

# 获取数据库用户


def get_user(db, username):
    if username in db:
        user_dict = db[username]
        return UserInDB(user_dict)

# 获取


def fake_decode_token(token: str):
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_schema)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={"WWW-Authenticate": "Bearer"}  # OAuth规范，应当加上
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Inactive user'
        )
    return current_user


@app06.post('/token')
async def login(form_data=Depends(OAuth2PasswordRequestForm)):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrent"
        )
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(user.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrent"
        )
    return {"access_token": user.username, "token_type": "bearer"}


@app06.get('/user/me')
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


""" 基于JWT的token验证 """

fake_users_db.update(
    {"john snow": {
        "username": "john snow",
        "full_name": "John Snow",
        "email": "johnsnow@example.com",
        "hashed_password": "$234ljlsajidooak",
        "disabled": False
    }}
)

SECRET_KEY = '0980sdf0sdf8sa0fa0s80a80sd98f0a'
ALGORITHM = 'HS256'  # 算法
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 过期时间


class Token(BaseModel):
    """返回给用户的token"""
    access_token: str
    token_type: str


pwd_context = CryptContext(schemes=['bcrypt'], deprecated=True)

oauth2_schema_jwt = OAuth2PasswordBearer(
    tokenUrl="/chapter06/jwt/token")  # 请求token的url地址


def vertify_password(plain_password, hashed_password):
    """对密码进行校验"""
    return pwd_context.verify(plain_password, hashed_password)


def jwt_get_user(db, username: str):
    """获取当前用户"""
    if username in db: #如果用户名在数据库的字典中
        user_dict = fake_users_db[username]#获取该用户的所有信息
        return UserInDB(**user_dict) #以UserInDB模型方式字典返回该用户的所有信息


def jwt_authenticate_user(db, username: str, password: str):
    """ 验证用户"""
    user = jwt_get_user(db=db, username=username) #从数据库中获取用户
    if not user: #用户不存在
        return False
    if not vertify_password(plain_password=password, hashed_password=user.hashed_password):#验证用户的密码
        return False
    return user #返回用户信息


def create_access_token(data: dict, expire_delta: Optional[timedelta] = None):
    """获取用户token"""
    to_encode = data.copy()#拷贝数据，浅拷贝
    if expire_delta: #传入了过期时间
        expire = datetime.utcnow()+expire_delta
    else: #没有传入过期时间，默认15分钟
        expire = datetime.utcnow()+timedelta(minutes=15)
    to_encode.update({'exp': expire})#更新过期时间到数据中
    encoded_jwt = jwt.encode(
        claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)#获取jwt编码
    return encoded_jwt


@app06.post('/jwt/token', response_model=Token)
async def login_for_access_token(form_data=Depends(OAuth2PasswordRequestForm)):#依赖OAuth2的Form
    """ 获取 token """
    user = jwt_authenticate_user(#验证用户
        db=fake_users_db, username=form_data.username, password=form_data.password)
    if not user:#验证未通过，抛出异常
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)#token过期时间
    access_token = create_access_token(#获取token 
        data={"sub": user.username}, expire_delta=access_token_expires
    )
    return {'token': access_token, 'token_type': "Bearer"}#返回token 和token 类型


async def jwt_get_current_user(token: str = Depends(oauth2_schema_jwt)):
    """获取当前用户，依赖于jwt token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY,
                             algorithms=[ALGORITHM])#解密
        username = payload.get("sub")#从解密信息中获得username
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = jwt_get_user(db=fake_users_db, username=username)
    if user is None:
        raise credentials_exception
    return user


async def jwt_get_current_active_user(current_user: User = Depends(jwt_get_current_user)):
    """获取当前激活用户，依赖于获取当前用户函数"""
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Inactive user'
        )
    return current_user

@app06.get('/jwt/user/me')
async def jwt_read_users_me(current_user: User = Depends(jwt_get_current_active_user)):
    """获取用户自己，依赖于当期激活用户"""
    return current_user