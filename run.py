#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :run.py
@说明        :项目入口文件，从这里启动
@时间        :2021/07/01 20:22:45
@作者        :张强
@版本        :1.0
'''
from starlette.applications import Starlette
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import HTTPException

from coronavirus import application
from tutorial import app03, app04, app05,app06


app = FastAPI(
    title='项目标题',
    description="项目的描述",
    version='1.0.1'
)
# mount表示将某个目录下一个完全独立的应用挂载过来，这个不会在API交互文档中显示
app.mount(path='/static',
          app=StaticFiles(directory='./coronavirus/static'), name='static')


@app.exception_handler(HTTPException)  # 重写HTTPException异常处理器
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)  # 重写请求验证异常处理器
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


# 生效子应用
# include_router 路由生效，第一个参数：子应用，第二个参数：路径前缀，第三个参数：文档标签
app.include_router(app03, prefix='/chapter03', tags=['第三章 请求参数与验证'])
app.include_router(app04, prefix='/chapter04', tags=['第四章 响应处理和FastAPI配置'])
app.include_router(app05, prefix='/chapter05', tags=['第五章 FastAPI的依赖注入系统'])
app.include_router(app06, prefix='/chapter06', tags=['第六章 安全、认证和授权'])
app.include_router(application, prefix='/chapter07', tags=['第七章 疫情数据跟踪器'])

if __name__ == '__main__':
    uvicorn.run('run:app',
                host='127.0.0.1',
                port=8001,
                reload=True,
                debug=True,
                workers=1)
