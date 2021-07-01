#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :run.py
@说明        :项目入口文件，从这里启动
@时间        :2021/07/01 20:22:45
@作者        :张强
@版本        :1.0
'''
import uvicorn
from fastapi import FastAPI

from tutorial import app03

app = FastAPI()

#生效子应用
app.include_router(app03,prefix='/chapter03',tags=['第三章 请求参数与验证']) #include_router 路由生效，第一个参数：子应用，第二个参数：路径前缀，第三个参数：文档标签


if __name__ == '__main__':
    uvicorn.run('run:app',
                host='127.0.0.1',
                port=8001,
                reload=True,
                debug=True,
                workers=1)
