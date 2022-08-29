import os
from pathlib import Path
from typing import Union
import json
import functions
from datetime import datetime, timedelta
from typing import List
import time
import subdomainfinder
import users
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from packages.database import engine, SessionLocal
from packages import crud, models, schemas
from packages import models
from fastapi import Depends, FastAPI, HTTPException, status,Request,BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
models.Base.metadata.create_all(bind=engine)
import validators
import subprocess


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(users.get_db)):
    user = users.authenticate_user(form_data.username, form_data.password,db)
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
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(users.get_db),User: schemas.User= Depends(users.get_current_active_admin)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(users.get_db),User: schemas.User= Depends(users.get_current_active_admin)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(users.get_db),User: schemas.User = Depends(users.get_current_active_user)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get('/me', summary='Get details of currently logged in user')
async def get_me(User: schemas.User = Depends(users.get_current_active_user)):
    return User

@app.post("/domain", summary='Scan for subdomain with subfinder tool')
def sub(domain: str,current_user: schemas.User = Depends(users.get_current_active_user)):
    return subdomainfinder.sub(domain,current_user)



@app.post("/nuclei")
async def backgrounded(config: schemas.NucleiConfig, back: BackgroundTasks ,current_user: schemas.User = Depends(users.get_current_active_user),db :Session= Depends(users.get_db)):
 back.add_task(run_nuclei,db,config,current_user)
 return("nuclei Started")

def run_nuclei(db,conf: schemas.NucleiConfig,user):

    urlsList = "./temp_files/"+functions.makefilename(conf.scan_name)+".txt"
    selected_tmp ="./temp_files/"+functions.makefilename(conf.scan_name)+"selected.txt"
    results= "./temp_files/"+functions.makefilename(conf.scan_name)+"results.txt"

    severtys = str(conf.severty).replace("[", '').replace("]", '').replace("'", '').replace(" ", '')
    if 'None' not in severtys:
        severtys ="-s "+severtys
    else:
        severtys=''
    for ts in conf.templates:
        if ts == 'None':
         templates = f'./temp_files/{functions.default_path(conf.scan_name)}'
         tsp = 'D'
         break
        else:
            tsp ='S'
            subprocess.check_output("echo " + ts + " >>"+ selected_tmp , shell=True)

    if tsp == 'D':
        tsp = templates
    else:
        if tsp == 'S':
         tsp = selected_tmp
         severtys = ''

    for domain in conf.domains: #Adding targets to file to be readed later
        subprocess.check_output("echo " + domain + " >>"+urlsList, shell=True)

    fetch_temp = open(tsp, "rt")
    scan_db=crud.add_scan(db,conf,user)
    for line in fetch_temp:

        cmd=f'./tools/nuclei -l {urlsList} -t {line.strip()} -json -o {results} {severtys}'

        #print (cmd)
        os.system(cmd)
        if Path(results).is_file():
            crud.vulns_to_db(db,results,scan_db.id) #Pass Results to database
            subprocess.check_output("rm " + results, shell=True)
        time.sleep(conf.time_delay)


    #clear temp files
    subprocess.check_output("rm " + urlsList+" "+ tsp, shell=True)



#subprocess.check_output("rm -f ./temp_files/urlsScan.txt", shell=True)
#subprocess.check_output("cat ./temp_files/selected_temps.txt", shell=True)

      #./nuclei -u https://sfzco.com -t /home/ya7ya/nuclei-templates/exposures/backups/zip-backup-files.yaml -json -o test.txt

# As a first domain name make directory with random numbers for storing selected templates temporary
