from typing import Optional

from app.crud.base import CRUDBase
from app.models import AssetType
from app.schemas import AssetCreate, AssetUpdate

from sqlalchemy.orm import Session


class CRUDAssetType(CRUDBase[AssetType, AssetCreate, AssetUpdate]):
    def get_by_name(self, db: Session, name: str) -> Optional[AssetType]:
        return db.query(self.model).filter(self.model.name == name).first()


asset_type = CRUDAssetType(AssetType)
