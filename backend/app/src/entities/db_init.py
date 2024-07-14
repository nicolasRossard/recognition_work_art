from sqlalchemy.orm import Session

import app.src.entities.models.user as user_model
import app.src.entities.models.original_art as original_art_model
from app.src.entities.database import engine
from app.src.services.tables.user import UserService
from app.config import SuperUser
from app.src.entities.schemas.user import UserCreate


def init_db(session: Session) -> None:
    # Create tables
    user_model.Base.metadata.create_all(bind=engine)
    original_art_model.Base.metadata.create_all(bind=engine)
    # check if superuser exists
    user = UserService(session).get_user_by_username(SuperUser.USERNAME)
    if not user:
        # create superuser
        user_to_create = UserCreate(
            username=SuperUser.USERNAME,
            password=SuperUser.PWD,
        )
        UserService(session).add(user_to_create)
