import uvicorn
import logging
from fastapi import FastAPI
#config
from config import APP_NAME, APP_DESCRIPTION, APP_VERSION, APP_TERMS_OF_SERVICE, APP_CONTACT_NAME, APP_CONTACT_EMAIL
#routes
from api import item_router
#database
from database.connection import engine
from database import  models
from database.connection import SessionLocal
#user request
import resource
resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

#create database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    terms_of_service=APP_TERMS_OF_SERVICE,
    contact={
        "name": APP_CONTACT_NAME,
        "email": APP_CONTACT_EMAIL,
    }
)

app.include_router(item_router)

@app.on_event('startup')
async def service_tasks_startup():
    """Start all the non-blocking service tasks, which run in the background."""
    pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
