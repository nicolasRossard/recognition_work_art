from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter
from app.src.services.authentification.auth import AuthService
from app.src.entities.database import dp_dependency

token_router = APIRouter(prefix="/token", tags=["login"], )


@token_router.post("/")
async def login(db: dp_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    return AuthService(db, form_data).login_user()
