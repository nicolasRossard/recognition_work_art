from fastapi import APIRouter, status

from app.src.entities.database import dp_dependency
from app.src.entities.schemas.original_art import OriginalArtCreate
from app.src.routers.controller import Controller
from app.src.services.authentification.auth import dp_user
from app.src.services.tables.original_art import OriginalArtService

original_art_router = APIRouter(prefix="/art", tags=["art"])


@original_art_router.post("/", status_code=status.HTTP_201_CREATED)
def create_mission(art_information: OriginalArtCreate, db: dp_dependency, _: dp_user):
    return Controller(service=OriginalArtService(db)).post(art_information)
