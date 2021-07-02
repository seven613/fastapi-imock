#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :chapter04.py
@说明        :
@时间        :2021/07/02 14:28:12
@作者        :张强
@版本        :1.0
'''


from typing import Optional, Union, List
from fastapi import APIRouter, status, Form, File, UploadFile,HTTPException

from pydantic import BaseModel, EmailStr

app04 = APIRouter()

"""  响应模型"""


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    mobile: str = "10086"
    address: str = None
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    mobile: str = "10086"
    address: str = None
    full_name: Optional[str] = None


users = {
    "user01": {"username": "user01", "password": "123123", "email": "user01@example.com"},
    "user02": {"username": "user02", "password": "123123", "email": "user02@example.com", "mobile": "110"}
}

# 路径操作


@app04.post("/response_model", response_model=UserOut, response_model_exclude_unset=True)
async def response_model(user: UserIn):
    """
    response_model_exclude_unset=True 表示默认值不包含在响应中，仅包含实际给的值
    """
    print(user.password)
    return users["user02"]


@app04.post(
    "/response_model/attributes", response_model=Union[UserIn, UserOut]
)
async def response_model_attributes(user: UserIn):
    del user.password  # 删除用户密码，否则就泄露了
    return user

"""  响应状态码  """


@app04.post("/status_code", status_code=200)
async def status_code():
    return{"status_code": 200}


@app04.post("/status_attribute", status_code=status.HTTP_200_OK)
async def status_attribute():
    print(type(status.HTTP_200_OK))
    return{"status_code": status.HTTP_200_OK}

"""  表单数据"""


@app04.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):  # 定义表单
    """ 用Form类需要安装pip intall python-multipart"""
    return{'username': username, "password": password}

""" 单文件、多文件上传及参数详解 """


@app04.post("/file")
async def file_(file: List[bytes] = File(...)):
    """ 使用File类 文件内容会以bytes的形式读入内存 适合于小文件"""
    return {"file_size": len(file)}


@app04.post('/upload_files')
async def upload_files(files: List[UploadFile] = File(...)):
    """
    使用UploadFile类的优势：
    1.文件存储在内存中， 使用的内存达到阈值后，将被保存在磁盘中
    2.适合于图片、视频大文件
    3.可以获取上传的文件的元数据，如文件名，创建时间等
    4.有文件对象的异步接口
    5.上传的文件是Python文件对象，可以使用write(),read(),seek(),close()操作
    """
    for file in files:
        contents = await file.read()
        print(contents)
    return{"filename": files[0].filename, "content_type": files[0].content_type}


"""  路径操作配置  """


@app04.post(
    "path_operation_configuration",
    response_model=UserOut,
    # tags=["Path", "Operation", "Configuration"],
    summary="This is summary",
    description="This is description",
    response_description="This is Response description",
    status_code=status.HTTP_200_OK,
    deprecated=True # 接口已经废弃，但是还能用
)
async def path_operation_configuration(user: UserIn):
    return user.dict()


""" 错误处理"""

@app04.get("/Http_exception")
async def http_exception(city:str):
    if city != "Beijing":
        raise HTTPException(status_code=404,detail="City not found!",headers={"x-error":'Error'})
    return city

@app04.get("/Http_exception/{city_id}")
async def override_http_exception(city_id:int):
    if city_id == 1:
        raise HTTPException(status_code=418,detail="Nope I don't like 1!",headers={"x-error":'Error'})
    return {'city_id':city_id}