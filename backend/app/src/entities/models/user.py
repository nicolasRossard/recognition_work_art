import json
import logging

import bcrypt

from sqlalchemy import Column, Integer, String, TIMESTAMP, func

from app.src.entities.database import Base
from app.src.utils.const import DATETIME_FORMAT, UPDATED_DATE_COMMENT, CREATED_DATE_COMMENT

logger = logging.getLogger(__name__)

created_date_comment = "Date of the creation of the field"
updated_date_comment = "Last updated date"
datetime_format = '%Y-%m-%dT%H:%M:%S:%f'


class User(Base):
    __tablename__ = "users"
    __table_args__ = {
        'comment': 'Table containing user information.'
    }
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True, comment="email or service name")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False,
                        comment=CREATED_DATE_COMMENT)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False,
                        comment=UPDATED_DATE_COMMENT)

    hash_password = Column(String, nullable=False)

    @staticmethod
    def set_password(password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.hash_password.encode('utf-8'))

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at.strftime(DATETIME_FORMAT),
            "updated_at": self.updated_at.strftime(DATETIME_FORMAT)
        }

    def to_json(self):
        return json.dumps(self.to_dict())