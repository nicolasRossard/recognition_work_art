import logging
from abc import ABC, abstractmethod
from typing import List

import sqlalchemy
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.src.entities.database import Base


class CRUDAbstractService(ABC):
    def __init__(self, session: Session, table: Base) -> None:
        self.session = session
        self.table = table
        self.logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    @abstractmethod
    def create_model(data: BaseModel):
        pass

    def add(self, data: BaseModel):

        model_data = self.create_model(data)

        try:
            self.session.add(model_data)
            self.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            filtered_data = {k: v for k, v in data.dict().items() if k != 'password'}
            self.logger.error("add :: SQLAlchemy integrity not respected\n"
                              f"-- data:\n{filtered_data}\n"
                              f"-- error:\n{e}\n--")
            return

        return model_data

    def get(self, id_: int):

        model_data = self.session.query(self.table).filter(self.table.id == id_).first()
        return model_data

    def delete(self, id_: int):
        model_data = self.session.query(self.table).filter(self.table.id == id_).first()
        if model_data:
            self.session.delete(model_data)
            self.session.commit()

    def update(self, id_: int, data: BaseModel):
        model_data = self.session.query(self.table).filter(self.table.id == id_).first()
        if model_data is not None:
            for key, value in data.model_dump().items():
                if value is not None:
                    setattr(model_data, key, value)
            self.session.commit()

            return model_data

    def all(self) -> List[dict]:
        all_data = self.session.query(self.table).all()
        return all_data
