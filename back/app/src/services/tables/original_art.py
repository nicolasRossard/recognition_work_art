from sqlalchemy.orm import Session

from app.src.entities.models.original_art import OriginalArt as ModelOriginalArt
from app.src.entities.schemas.original_art import OriginalArtCreate
from app.src.services.tables.crud_abstract import CRUDAbstractService


class OriginalArtService(CRUDAbstractService):

    def __init__(self, session: Session) -> None:
        super().__init__(session, ModelOriginalArt)

    @staticmethod
    def create_model(art_information: OriginalArtCreate) -> ModelOriginalArt:

        model_art = ModelOriginalArt(
            filepath=art_information.filepath,
            explanation=art_information.explanation,
            author=art_information.author,
            gen_description=art_information.gen_description,
        )
        return model_art

