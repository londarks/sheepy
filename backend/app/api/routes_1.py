from fastapi import APIRouter
import logging
import utilities as  schemas

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

router = APIRouter()


@router.post("/auth/login", tags=["Sheepy"])
async def login(register: schemas.Login):
    """ Teste function"""
    return {"Hello word"}


@router.post("/signup", tags=["Sheepy"])
async def register(register: schemas.Register):
    """ Teste function"""
    return {"Hello word"}
