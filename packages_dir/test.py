
from sqlalchemy.orm import Session
import json

from packages_dir import models_dir, schemas_dir
import users

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User_t).offset(skip).limit(limit).all()
get_users()
