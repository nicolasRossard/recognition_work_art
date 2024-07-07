from app.src.entities import models
from sqlalchemy.orm import Session
from app.src.entities.database import engine
from app.src.service.tables.user import UserService
from app.config import SuperUser
from app.src.entities.schemas.user import UserCreate
from app.src.service.authentification.user import UserRole


def init_db(session: Session) -> None:
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    # check if superuser exists
    user = UserService(session).get_user_by_username(SuperUser.USERNAME)
    if not user:
        # create superuser
        user_to_create = UserCreate(
            username=SuperUser.USERNAME,
            role=UserRole.admin,
            password=SuperUser.PWD,
        )
        UserService(session).add(user_to_create)
