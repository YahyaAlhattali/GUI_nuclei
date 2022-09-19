
from sqlalchemy.orm import Session
import json
import users
from packages_dir import models_dir
from packages_dir import database
import subprocess

def get_user(db: Session, user_id: int):
    return db.query(models_dir.User).filter(models_dir.User.id == user_id).first()


def get_user_by_username(db: Session,username: str):
    return db.query(models_dir.User).filter(models_dir.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    print(db)
    #ds= Session (Depends( users.get_db))
    #print(ds)
    return db.query(models_dir.User).offset(skip).limit(limit).all()


def create_user(db: Session, user):
    hashed_password = users.get_password_hash(user.password)
    db_user = models_dir.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models_dir.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item, user_id: int):
    db_item = models_dir.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
def add_scan(scan_data,user):


    #
    # # SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    # SQLALCHEMY_DATABASE_URL = "postgresql://ya7ya:123456@localhost/xtool"
    #
    # engine = create_engine(
    #     SQLALCHEMY_DATABASE_URL
    # )
    # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    #
    #
    #
    #
    # metadata = MetaData(engine)
    # Base = declarative_base()

    with Session(database.engine) as session:
     #db= Session (Depends( users.get_db))
     #print(f'Session: {db}')
     scan=models_dir.Scan(main_domain=scan_data.main_domain,scan_name=scan_data.scan_name,progress_status=scan_data.progress_status,description=scan_data.description,user_id=user.id)
     #print(Sessionx)
     session.add(scan)
     session.commit()
     session.refresh(scan)
    return scan
def update_scan_progress(id,progress):
    #db= Session (Depends( users.get_db))
    with Session(database.engine) as session:
     prog = session.query(models_dir.Scan).filter(models_dir.Scan.id==id).first()
     prog.progress_status = f'{progress}'
     print(prog)
     session.commit()
     session.refresh(prog)
    return None
def vulns_to_db(result,scan_id):
 #db = Session(Depends(users.get_db))
    #input file
 fin = open(result, "rt")


 for line in fin:
      #print (type(line))
      json_object = json.loads(line)
      #data = json.loads(json_object)
      #if json_object["info"]["CVSS_Score"] not in json_object: cvss ='None'
      if "description" in json_object["info"]:
         Description = json_object["info"]["description"]
      else:
          Description = 'None'

      with Session(database.engine) as session:
           db_item = models_dir.Vulnerabilities(scan_id=scan_id,Type=json_object["type"],Title=json_object["info"]["name"],Vulnerable_URL=json_object["matched-at"],Description=Description,Severity=json_object["info"]["severity"],template_used=json_object["template-id"])
           session.add(db_item)
           session.commit()
           session.refresh(db_item)
 subprocess.check_output("rm " + result, shell=True)
 return "Started"




