from fastapi import APIRouter
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

router = APIRouter()


@router.get("/", tags=["Sheepy"])
async def home():
    """ Teste function"""
    return {"Helloe word"}
