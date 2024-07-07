from sqlalchemy.orm import Session

from app.src.entities.database import Base
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
            role=user.role
        )

        return model_user

    def get_user_by_username(self, username: str) -> Base:
        model_data = self.session.query(self.table).filter(self.table.username == username).first()
        return model_data
