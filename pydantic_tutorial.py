#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :pydantic_tutorial.py
@说明        :
@时间        :2021/07/01 15:48:53
@作者        :张强
@版本        :1.0
'''

from datetime import datetime, date
from pydantic import BaseModel, ValidationError, constr
from pathlib import Path
from typing import Optional, List
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import null


class User(BaseModel):
    id: int
    name: str = "John Snow"
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


external_data = {
    "id": "123",
    "signup_ts": "2021-07-01 15:50",
    "friends": [1, 2, "3"]
}

user = User(**external_data)
print(user.id, user.friends)
print(repr(user.signup_ts))
print(user.dict())


try:
    User(id=1, signup_ts=datetime.today(), friends=[1, 2, 'no number'])
except ValidationError as e:
    print(e.json())  # 转换成json格式

print(user.dict())
print(user.json())
print(user.copy())  # 浅拷贝
print('-------------------------------------')
print('解析对象：User.parse_obj(obj=external_data) -->',
      User.parse_obj(obj=external_data))
print('解析字符串：User.parse_raw({"id": 123, "name": "John Snow", "signup_ts": "2021-07-01T15:50:00", "friends": [1, 2, 3]}) -->', User.parse_raw(
    '{"id": 123, "name": "John Snow", "signup_ts": "2021-07-01T15:50:00", "friends": [1, 2, 3]}'))

path = Path('pydantic_tutorial.json')
path.write_text(
    '{"id": 123, "name": "John Snow", "signup_ts": "2021-07-01T15:50:00", "friends": [1, 2, 3]}')
print('解析文件：User.parse_file(文件名) -->', User.parse_file(path))

print('-------------------------------------')
print('user.schema() -->', user.schema())
print('user.schema_json() -->', user.schema_json())

print('-------------------------------------')

print(User.__fields__.keys())  # 打印字段顺序，与定义顺序一致

print('\033[31m4.---递归模型 ---\033[0m')


class Sound(BaseModel):
    sound: str


class Dog(BaseModel):
    birthday: date
    weight: float = Optional[None]
    sound: List[Sound]  # 叫声不同，递归模型，一个嵌套另一个类


dogs = Dog(birthday=date.today(), weight=6.66, sound=[
    {"sound": "wang wang ~~"}, {"sound": "wu wu ~~"}])
print(dogs.dict())
print('\033[31m5.---ORM模型：从类实例创建符合ORM对象的模型 ---\033[0m')

Base = declarative_base()

#定义了数据库表结构
class CompanyOrm(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    name = Column(String(63), unique=True)
    domains = Column(ARRAY(String(255)))

#定义与数据库表相关联的模型类，
class CompandMode(BaseModel):
    id: int
    public_key: constr(max_length=20)
    name: constr(max_length=63)
    domains: List[constr(max_length=255)]

    class Config: #启用orm关联
        orm_mode = True

#伪造数据
co_orm = CompanyOrm(
    id=123,
    public_key="foobar",
    name="Testing",
    domains=['example.com', '163.com']
)
print(CompandMode.from_orm(co_orm))#输出模型类格式的数据
