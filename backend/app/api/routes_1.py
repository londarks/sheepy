import logging
from utilities import  UserCreate, Login, create_user
from fastapi import APIRouter, Depends, status
from core import jwt_token_required, create_jwt_token, create_refresh_token
#database
from database import  crud
from database.connection import SessionLocal
from sqlalchemy.orm import Session

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

router = APIRouter()

def get_database_session() -> Session:
    """
    Retorna uma sessão de banco de dados para ser usada em um contexto com.

    Returns:
        Uma sessão de banco de dados.
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        if not database.is_active:
            database.close()

@router.get("/", tags=["Sheepy"])
@jwt_token_required
async def home(payload: dict):
    return {"message": "home from api"}

@router.post("/auth/login", tags=["Sheepy"])
async def login(register: Login):
    """ Teste function"""
    return {"message": "login!"}


@router.post("/signup",status_code=status.HTTP_201_CREATED, tags=["Sheepy"])
async def register(register: UserCreate, Database: str = Depends(get_database_session)):
    """ Teste function"""
    token = create_user(Database=Database, user=register)
    return token
