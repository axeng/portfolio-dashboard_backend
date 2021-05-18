from typing import Optional

from app.crud.base import CRUDBase
from app.models import Asset
from app.schemas import AssetCreate, AssetUpdate

from sqlalchemy.orm import Session


class CRUDAsset(CRUDBase[Asset, AssetCreate, AssetUpdate]):
    def get_by_code(self, db: Session, code: str) -> Optional[Asset]:
        return db.query(self.model).filter(self.model.code == code).first()


asset = CRUDAsset(Asset)
