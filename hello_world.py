#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :hello_world.py
@说明        :
@时间        :2021/07/01 16:21:39
@作者        :张强
@版本        :1.0
'''
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class CityInfo(BaseModel):
    province: str
    country: str
    is_affected: Optional[bool] = None


@app.get('/')
async def hello_world():
    return{'hello', 'world'}


@app.get('/city/{city}')
async def result(city: str, query_string: Optional[str] = None): #注意写法Optional不能放到等号后面
    return{'city': city, 'query_string': query_string}


@app.put('/city/{city}')
async def result(city:str,city_info:CityInfo):
  return {'city':city,'country':city_info.country,'is_affected':city_info.is_affected}
