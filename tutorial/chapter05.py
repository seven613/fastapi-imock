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
from fastapi import APIRouter, Depends, Header, HTTPException

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
# #以下三种写法相同
# async def class_as_dependencies(commons:CommonQueryParams=Depends(CommonQueryParams)):#写法1
# async def class_as_dependencies(commons:CommonQueryParams=Depends()):#写法2
async def class_as_dependencies(commons=Depends(CommonQueryParams)):  # 写法3，
    response = {}
    if commons.q:
        response.update({'q': q})
    items = fake_items_db[commons.page:commons.page+commons.limit]
    response.update({'items': items})
    return items

""" 子依赖"""
# 1.定义函数


def query(q: Optional[str] = None):
    return q
# 定义子依赖函数


def sub_query(q: str = Depends(query), last_query: Optional[str] = None):
    if not q:
        return last_query
    return q


@app05.get('/sub_dependency')
async def sub_dependency(final_query=Depends(sub_query, use_cache=True)):  # 使用子依赖，
    """use_cache=True表示多个依赖有一个共同的子依赖时，每次request只调用子依赖一次，多次调用从缓存中读取"""
    return {"sub_dependency": final_query}

"""路径操作装饰器中的依赖"""


async def verify_token(x_token: str = Header(...)):
    """没有返回值的子依赖"""
    if x_token != 'fake-super-secret-token':
        raise HTTPException(status_code=400, detail="X-token header invalid")
    return x_token


async def verify_key(x_key: str = Header(...)):
    """有返回值的子依赖，但是返回值不会被依赖"""
    if x_key != 'fake-super-secret-key':
        raise HTTPException(status_code=400, detail="X-key header invalid")
    return x_key


@app05.get('/dependency_in_path_operation', dependencies=[Depends(verify_token), Depends(verify_key)])
async def dependency_in_path_operation():
    return[{'user01': 'user01'}, {'user02': 'user02'}]

""" 全局依赖 """

# app05=APIRouter(dependencies=[Depends(verify_token),Depends(verify_key)])# 全局依赖

""" 使用yield的子依赖"""
# 伪代码


async def get_db():
    db = 'db_connect'
    try:
        yield db
    finally:
        db.endswith('db_close')


async def dependency_a():
    dep_a = "generate_dep_a()"#生成依赖dep_a
    try:
        yield dep_a
    finally:
        dep_a.endswith('db_close')


async def dependency_b(dep_a=Depends(dependency_a)):
    dep_b = "generate_dep_b()" #生成新的依赖dep_b
    try:
        yield dep_b
    finally:
        dep_b.endswith(dep_a) #这里关闭的是子依赖dep_a

async def dependency_c(dep_b=Depends(dependency_b)):
    dep_c = "generate_dep_c()" #生成新的依赖dep_c
    try:
        yield dep_c #可以全文引用dep_c
    finally:
        dep_c.endswith(dep_b) #这里关闭的是子依赖dep_a