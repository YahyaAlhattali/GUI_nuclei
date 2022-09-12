import math
import os,sys
from pathlib import Path
import functions
from datetime import datetime, timedelta
from typing import List

import packages_dir.schemas_dir
import subdomainfinder
import users,core_function
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from packages_dir.database import engine, SessionLocal
import packages_dir.schemas_dir as schemas
from packages_dir import crud, models_dir
from fastapi import Depends, FastAPI, HTTPException, status, Request, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
models_dir.Base.metadata.create_all(bind=engine)
import subprocess
from redis import Redis
from rq import Queue
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
redis_conn = Redis()
q = Queue(connection=redis_conn)  # no args implies the default queue


@app.post("/token", response_model=packages_dir.schemas_dir.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(users.get_db)):
    user = users.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=users.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = users.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/", response_model=schemas.User_t)
def create_user(user: packages_dir.schemas_dir.UserCreate, db: Session = Depends(users.get_db),
                User: schemas.User_t = Depends(users.get_current_active_admin)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User_t])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(users.get_db),
               User: schemas.User_t = Depends(users.get_current_active_admin)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User_t)
def read_user(user_id: int, db: Session = Depends(users.get_db),
              User: schemas.User_t = Depends(users.get_current_active_user)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get('/me', summary='Get details of currently logged in user')
async def get_me(User: schemas.User_t = Depends(users.get_current_active_user)):
    return User


@app.post("/domain", summary='Scan for subdomain with subfinder tool')
def sub(domain: str, current_user: schemas.User_t = Depends(users.get_current_active_user)):
    return subdomainfinder.sub(domain, current_user)
@app.post("/update", summary='Update db')
def sub(id: int,pros: str,db: Session = Depends(users.get_db)):

    return crud.update_scan_progress(id,pros,db)

@app.post("/nuclei")
async def start_new_scan(config: schemas.NucleiConfig,
                         db: Session = Depends(users.get_db),
                         User: schemas.User_t = Depends(users.get_current_active_user)):
    # back.add_task(run_nuclei,db,config,current_user)
    try:
        job = q.enqueue(core_function.run_nuclei,config, db,User)
        #print(job.result)
        #job = q.enqueue(blengbleng, "Yahya")
    except Exception as e :
        print(e)
        time.sleep(5)
    # job = q.enqueue( run_nuclei, config.dict(),current_user)
    # blengbleng(config.scan_name)
    return (f'nuclei job')


def blengbleng(name):
    print(name)

