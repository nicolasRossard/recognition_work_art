from fastapi import FastAPI

from app.src.entities.db_init import init_db

from app.src.entities.database import SessionLocal

app = FastAPI()

init_db(SessionLocal())