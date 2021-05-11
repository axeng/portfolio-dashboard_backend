from typing import Optional

from app.crud.commons import CRUDBase
from app.models import Asset
from app.schemas import AssetCreate, AssetUpdate

from sqlalchemy.orm import Session


class CRUDAsset(CRUDBase[Asset, AssetCreate, AssetUpdate]):
    def get_by_code(self, db: Session, code: str) -> Optional[Asset]:
        return db.query(Asset).filter(Asset.code == code).first()


asset = CRUDAsset(Asset)
