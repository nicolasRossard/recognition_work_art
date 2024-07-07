from datetime import datetime
from pydantic import BaseModel


class OriginalArtBase(BaseModel):
    filepath: str
    explanation: str
    author: str
    gen_description: str


class OriginalArtCreate(OriginalArtBase):
    pass


class OriginalArtUpdate(OriginalArtBase):
    pass


class OriginalArtDB(OriginalArtBase):
    id: int
    created_at: datetime
    updated_at: datetime
