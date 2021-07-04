#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :database.py
@说明        :数据库配置文件
@时间        :2021/07/04 10:45:55
@作者        :张强
@版本        :1.0
'''


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./coffonairus.sqlite3"

engine = create_engine(

    # echo=True 表示数据库引擎将使用repr()函数记录所有sql语句及参数列表到日志
    # sqlalchemy是多线程的，指定check_same_thread=False来让建立的对象任意线程都可以使用，这个参数是sqlite才使用的
    SQLALCHEMY_DATABASE_URL, encoding='utf-8', echo=True, connect_args={'check_same_thread': False}
)
# 在sqlalchemy中，CRUD都是通过会话(session)进行的，所以必须先创建会话，每一个SessionLocal实例就是一个数据
SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, expire_on_commit=True)


# 创建基本的映射类
Base = declarative_base(bind=engine, name='Base')
