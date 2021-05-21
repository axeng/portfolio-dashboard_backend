from typing import Optional, Dict

from app.crud.base import CRUDBase
from app.models import AssetType
from app.schemas import AssetCreate, AssetUpdate

from sqlalchemy.orm import Session


class CRUDAssetType(CRUDBase[AssetType, AssetCreate, AssetUpdate]):
    def get_by_name(self, db: Session, name: str) -> Optional[AssetType]:
        return db.query(self.model).filter(self.model.name == name).first()

    def get_dict(self, db: Session) -> Dict[str, int]:
        type_list = db.query(self.model).all()
        type_dict = {}

        for item in type_list:
            type_dict[item.name] = item.id

        return type_dict


asset_type = CRUDAssetType(AssetType)
