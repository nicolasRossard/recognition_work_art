import json
import logging

from sqlalchemy import Column, Integer, String, TIMESTAMP, func

from app.src.entities.database import Base
from app.src.utils.const import DATETIME_FORMAT, UPDATED_DATE_COMMENT, CREATED_DATE_COMMENT

logger = logging.getLogger(__name__)


class OriginalArt(Base):
    __tablename__ = "original_arts"
    __table_args__ = {
        'comment': 'Table containing all original arts and their information.'
    }
    id = Column(Integer, primary_key=True, nullable=False, comment="ID generated when creating element")

    filepath = Column(String, nullable=False, comment="Relative filepath of the image")
    explanation = Column(String, nullable=False, comment="Text which explained the original art")
    author = Column(String, nullable=False, comment="Author information")
    gen_description = Column(String, nullable=False, comment="Description generated by the LLM")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False,
                        comment=CREATED_DATE_COMMENT)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False,
                        comment=UPDATED_DATE_COMMENT)

    def to_dict(self):
        return {
            "id": self.id,
            "filepath": self.filepath,
            "explanation": self.explanation,
            "author": self.author,
            "gen_description": self.gen_description,
            "created_at": self.created_at.strftime(DATETIME_FORMAT),
            "updated_at": self.updated_at.strftime(DATETIME_FORMAT)
        }

    def to_json(self):
        return json.dumps(self.to_dict())
