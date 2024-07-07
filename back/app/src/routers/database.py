from fastapi import APIRouter, status

from app.src.entities.database import dp_dependency
from app.src.entities.schemas.original_art import OriginalArtCreate
from app.src.services.authentification.auth import dp_user

art_database_router = APIRouter(prefix="/art", tags=["art"])

@art_database_router.post("/", status_code=status.HTTP_201_CREATED)  # todo add responses into api
def create_mission(art_information: OriginalArtCreate, db: dp_dependency, user: dp_user):
    return Controller(service=MissionService(db)).post(art_information)