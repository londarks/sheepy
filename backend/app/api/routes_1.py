import logging
import utilities as  schemas
from fastapi import APIRouter
from core import PasswordManager, jwt_token_required, create_jwt_token
#database
from database import  crud
from database.connection import SessionLocal

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

router = APIRouter()
Database = SessionLocal()

@router.get("/", tags=["Sheepy"])
@jwt_token_required
async def home(payload: dict):
    return {"message": "home from api"}

@router.post("/auth/login", tags=["Sheepy"])
async def login(register: schemas.Login):
    """ Teste function"""
    return {"message": "login!"}


@router.post("/signup", tags=["Sheepy"])
async def register(register: schemas.UserRegister):
    """ Teste function"""
    try:
        crud.get_user_by_email_register(db=Database, email=register.email)
        register.password = PasswordManager.hash_password(password=register.password)
        crud.create_user(db=Database, register=register)
        user = crud.get_user_by_email(db=Database, email=register.email)
        token = create_jwt_token(user_id=user.id)
        return {'bearer': token}
    except ValueError as e:
        return {'error': f'{e}'}
