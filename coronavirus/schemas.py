#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :schemas.py
@说明        :pydantic模型类
@时间        :2021/07/04 10:45:24
@作者        :张强
@版本        :1.0
'''

from datetime import datetime
from datetime import date as date_

from pydantic import BaseModel


class CreateData(BaseModel):
    date: date_
    confiremd: int = 0
    deaths: int = 0
    recoverd: int = 0


class CreateCity(BaseModel):
    province: str
    country: str
    country_code: str
    country_popuation: int


class ReadData(CreateData):
    id: int
    city_id: int
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True


class ReadCity(CreateCity):
    id: int
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True
