from sqlalchemy.orm import Session

from app.src.entities.models import User as ModelUser
from app.src.entities.schemas.user import UserCreate
from app.src.services.tables.crud_abstract import CRUDAbstractService


class UserService(CRUDAbstractService):

    def __init__(self, session: Session) -> None:
        super().__init__(session, ModelUser)

    @staticmethod
    def create_model(user: UserCreate) -> ModelUser:

        model_user = ModelUser(
            username=user.username,
            hash_password=ModelUser.set_password(user.password),
        )

        return model_user

