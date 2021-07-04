#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :models.py
@说明        :数据类
@时间        :2021/07/04 10:45:39
@作者        :张强
@版本        :1.0
'''

from sqlalchemy import Column, String, Integer, BigInteger, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from .database import Base


class City(Base):
    __tablename__ = 'city'  # 数据表名
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    province = Column(String(100), unique=True, nullable=True, comment="省/直辖市")
    country = Column(String(100), nullable=False, comment='国家')
    country_code = Column(String(100), nullable=False, comment='国家代码')
    country_popuation = Column(BigInteger, nullable=False, comment='国家人口')
    data = relationship('Data', back_populates='city')

    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(),
                        onupdate=func.now(), comment='更新时间')

    __maper_args__ = {"order_by": country_code}

    def __repr__(self):
        return f'{self.country}_{self.province}'


class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey('city.id'), comment='所属省/直辖市')
    date = Column(Date, nullable=False, comment='数据日期')
    confiremd = Column(BigInteger, default=0, nullable=False, comment='确诊数量')
    deaths = Column(BigInteger, default=0, nullable=False, comment='死亡数量')
    recoverd = Column(BigInteger, default=0, nullable=False, comment='痊愈数量')
    city = relationship('City', back_populates='data')

    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(),
                        onupdate=func.now(), comment='更新时间')

    __maper_args__ = {"order_by": date.desc()}

    def __repr__(self):
        return f'repr({self.date}):确诊{self.comfired}例'
