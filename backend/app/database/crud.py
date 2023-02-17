from sqlalchemy.orm import Session
from . import models

def get_all_user(db: Session):
    return db.query(models.User).all()

def get_user(db: Session, id_user: str):
    return db.query(models.User).filter(models.User.id_user == id_user).first()