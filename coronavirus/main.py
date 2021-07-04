#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :main.py
@说明        :项目主文件
@时间        :2021/07/04 10:46:20
@作者        :张强
@版本        :1.0
'''
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status,Request

from sqlalchemy.orm import Session

from fastapi.templating import Jinja2Templates
from coronavirus import crud, schemas
from coronavirus.database import engine, Base, SessionLocal
from coronavirus.models import City, Data

application = APIRouter()

templates=Jinja2Templates(directory='./coronavrius/templates')

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@application.post('/create_city', response_model=schemas.ReadCity)
async def create_city(city: schemas.CreateCity, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, name=city.province)
    if db_city:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ciyt alread registed"
        )
    return crud.create_city(db=db, city=city)


@application.get('/get_city/{city}', response_model=schemas.ReadCity)
async def get_city(city: str, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, name=city)
    if db_city is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="city not found"
        )
    return db_city


@application.get('/get_cities', response_model=List[schemas.ReadCity])
async def get_cities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cities = crud.get_cities(db=db, skip=skip, limit=limit)
    return cities

# -----------------------------------------------------


@application.post('/create_data', response_model=schemas.ReadData)
async def create_data(city: str, data: schemas.CreateData, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, name=city)
    data = crud.create_city_data(db=db, data=data, city_id=city.id)
    return data


@application.get('/get_data')
async def get_data(city: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = crud.get_data(db=db, city=city, skip=skip, limit=limit)
    return data


@application.get('/')
async def coronavirus(request:Request,city:str=None,skip:int=0,limit:int=100,db:Session=Depends(get_db)):
    data = crud.get_data(db=db, city=city, skip=skip, limit=limit)
    return templates.TemplateResponse('home.html',{
        "request":request,
        "data":data,
        "sync_data_url":"/coronavirus/sync_coronavirus_data/jhu"
    })