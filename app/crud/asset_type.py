from typing import Optional

from app.crud.commons import CRUDBase
from app.models import AssetType
from app.schemas import AssetCreate, AssetUpdate

from sqlalchemy.orm import Session


class CRUDAssetType(CRUDBase[AssetType, AssetCreate, AssetUpdate]):
    def get_by_name(self, db: Session, name: str) -> Optional[AssetType]:
        return db.query(AssetType).filter(AssetType.name == name).first()


asset_type = CRUDAssetType(AssetType)
