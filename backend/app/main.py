from fastapi import FastAPI

from app.src.entities.db_init import init_db

from app.src.entities.database import SessionLocal
from app.src.routers.auth import token_router
from app.src.routers.original_art import original_art_router

app = FastAPI()

init_db(SessionLocal())

app.include_router(original_art_router)
app.include_router(token_router)
