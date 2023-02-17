from fastapi import APIRouter
import logging
import aiohttp
import sys


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

router = APIRouter()
# Database = SessionLocal()


@router.get("/", tags=["Obsignal"])
async def home():
    """ Teste function"""
    return {"Helloe word"}
