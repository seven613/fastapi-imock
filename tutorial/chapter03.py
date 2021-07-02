#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :chapter03.py
@说明        :子应用
@时间        :2021/07/01 20:30:48
@作者        :张强
@版本        :1.0
'''
from datetime import date
from enum import Enum
from typing import Optional, List
from fastapi import APIRouter, Path, Query, Cookie, Header
from pydantic import BaseModel, Field

app03 = APIRouter()
"""  路径参数和数字验证"""


@app03.get('/path/parameters')
def path_parameters():
    return {'message': 'this is a message'}


# 注意路由顺序
@app03.get('/path/{parameters}')  # 假如 路径参数=paramenters，那么响应会被上一个函数匹配
def path_parameters(parameters: str):
    return {'message': parameters}


class CityName(str, Enum):
    Beijing = "Beijing China"
    Shanghai = "Shanghai China"
    London = "London UK"


@app03.get('/enum/{city}')
async def latest(city: CityName):
    if city == CityName.London:
        return {'city_name': city, 'confirmed': 1497, 'death': 7000}
    if city == CityName.Beijing:
        return {'city_name': city, 'confirmed': 234, 'death': 0}
    return {'city_name': city, 'latest': 'unknown'}


@app03.get('/files/{file_path:path}')  # 传递文件路径,必须用:path
async def filepath(file_path: str):
    return f"This file path is {file_path}"


# 路径参数验证，使用Path，与file_path:path不一样
@app03.get('/path_num_validate/{num}')
def path_params_validate(
        num: int = Path(
            ...,  # ...必填，不允许为空
            title="Your number",
            description="不可描述",
            ge=2,  # 大于等于2
            le=10)):  # 小于等于2
    return num


""" 查询参数和字符串验证"""


@app03.get('/query')
def page_limit(page: int = 1, limit: Optional[int] = None):
    if limit:
        return {'page': page, 'limit': limit}
    return {'page': page}


# bool类型转换
@app03.get('/query/bool/conversion')
def type_conversion(
        param: bool = False):  # yes、True、1、On都被转为True，其他的报错或被转为False
    return param


@app03.get('/query/validations')
def query_params_validate(
        value: str = Query(..., max_length=10, min_length=2),  # 参数验证，使用Query
        values: List[str] = Query(default=['v1', 'v2'],
                                  alias="alias_name")):  # 多个参数的列表，参数别名
    return value, values


"""  请求体和字段"""


class CityInfo(BaseModel):
    name: str = Field(..., example="Beijing")  # example 注解，不会被验证
    country: str
    country_code: str = None
    country_population: int = Field(default=800,
                                    title="人口数量",
                                    description="国家的人口数量，必须大于800")

    class Config:  # 定义模型的额外信息
        schema_extra = {
            "example": {  # 定义模型样例
                "name": "Beijing",
                "country": "China",
                "country_code": "CN",
                "country_population": 14000000000
            }
        }


@app03.post('/request_body/city')
def city_info(city: CityInfo):
    return city.dict()


"""  请求体、路径参数、查询参数 混合"""


@app03.put('/request_body/city/{name}')
def mix_city_info(
    name: str,
    city01: CityInfo,
    city02: CityInfo,
    confirmed: int = Query(ge=0, description="确诊数", default=0),
    death: int = Query(ge=0, description="死亡数", default=0)
):
    if name == "Shanghai":
        return {"Shanghai": {"confirmed": confirmed, "death": death}}
    return city01.dict(), city02.dict()


"""  数据格式嵌套的请求体"""


class Data(BaseModel):
    city: List[CityInfo] = None
    date: date
    confirmed: int = Field(ge=0, description="确诊数", default=0)
    deaths: int = Field(ge=0, description="死亡数", default=0)
    recovered: int = Field(ge=0, description="痊愈数", default=0)


@app03.put('/request_body/nested')
def nested_models(data: Data):
    return data


"""  Cookie 和 Header"""


@app03.get('/cookie/')  # 只能用PostMan测试
def cookie(cookie_id: Optional[str] = Cookie(None)):
    return {"cookie_id": cookie_id}


@app03.get('/header')
def header(user_agent: Optional[str] = Header(None, convert_underscores=True), x_token: List[str] = Header(None)):
    return{"User-Agent": user_agent, "x_token": x_token}
