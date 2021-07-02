#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :chapter05.py
@说明        :
@时间        :2021/07/02 14:27:40
@作者        :张强
@版本        :1.0
'''

from typing import Optional
from fastapi import APIRouter, Depends

app05 = APIRouter()


""" 创建、导入和声明依赖"""

# 定义依赖函数


async def common_parameters(q: Optional[str] = None, page: int = 1, limit: int = 10):
    return{'q': q, 'page': page, "limit": limit}


@app05.get('/dependency01')
async def dependency01(commons: dict = Depends(common_parameters)):  # 异步函数使用依赖
    return commons


@app05.get('/dependency02')
def dependency02(commons: dict = Depends(common_parameters)):  # 非异步函数使用依赖
    return commons


""" 将类作为依赖项"""

fake_items_db = [{'item_name': "Foo"}, {
    "item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, page: int = 1, limit: int = 10):
        self.q = q
        self.page = page
        self.limit = limit
@app05.get("/classes_as_dependencies")
async def class_as_dependencies(commons:CommonQueryParams=Depends(CommonQueryParams)):
async def class_as_dependencies(commons:CommonQueryParams=Depends(CommonQueryParams)):
async def class_as_dependencies(commons:CommonQueryParams=Depends(CommonQueryParams)):