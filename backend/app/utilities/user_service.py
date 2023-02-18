from sqlalchemy.orm import Session
from core import PasswordManager, jwt_token_required, create_jwt_token, create_refresh_token
import utilities as  schemas
#database
from database import  crud
from database import models

def create_user(Database: Session, user: schemas.UserCreate):
    try:
        search = Database.query(models.User).filter(models.User.email == user.email).first()
        if search:
            raise ValueError("User already existsd")
        user.password = PasswordManager.hash_password(password=user.password)
        crud.create_user(db=Database, register=user)
        user = crud.get_user_by_email(db=Database, email=user.email)
        token = create_jwt_token(user_id=user.id)
        refresh_token = create_refresh_token(user_id=user.id)
        return {'bearer': token}

    except ValueError as e:
        return {'error': f'{e}'}
    
    except Exception as e:
        return {'error': f'{e}'}