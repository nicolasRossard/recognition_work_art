import logging

from fastapi import HTTPException, status
from pydantic import BaseModel
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self, service):
        self.service = service

    def post(self, data: BaseModel):

        model_data = self.service.add(data)

        if model_data is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="SQLALCHEMY Integrity error"
            )

        return JSONResponse(content=model_data.to_dict(), status_code=status.HTTP_201_CREATED)

    def get(self, id_: int):
        model_data = self.service.get(id_)

        if model_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ID {id_} not found"
            )
        return JSONResponse(content=model_data.to_dict(), status_code=status.HTTP_200_OK)

    def delete(self, id_: int):
        dict_data = self.service.get(id_)

        if dict_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ID {id_} not found"
            )

        self.service.delete(id_)

        return JSONResponse(content={"message": f"ID {id_} deleted"}, status_code=status.HTTP_200_OK)

    def all(self):
        model_data = self.service.all()
        return JSONResponse(content=[data.to_dict() for data in model_data], status_code=status.HTTP_200_OK)

    def put(self, id_: int, data: BaseModel):

        model_data = self.service.update(id_, data)

        if model_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ID {id_} not found"
            )

        return JSONResponse(content=model_data.to_dict(), status_code=status.HTTP_200_OK)
