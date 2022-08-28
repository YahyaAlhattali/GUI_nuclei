
from sqlalchemy.orm import Session
import json
import main
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session,username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = main.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
def add_scan(db: Session,scan_data):
    scan=models.Scan(main_domain=scan_data.main_domain,scan_name=scan_data.scan_name,progress_status=scan_data.progress_status,description)
    db.add(scan)
    db.commit()
    db.refresh(scan)

def vulns_to_db(db: Session,result,scan_name):
#input file
 fin = open(result, "rt")


 for line in fin:
      #print (type(line))
      json_object = json.loads(line)
      #data = json.loads(json_object)

      db_item = models.Vulnerabilities(Type=json_object["host"],scan_id=scan_name)
      db.add(db_item)
      db.commit()
      db.refresh(db_item)
      print(f'{json_object["host"]} {json_object["info"]["name"]}')
      return db_item




