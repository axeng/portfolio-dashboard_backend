from app.crud.commons import CRUDBase
from app.models import AssetType
from app.schemas import AssetCreate, AssetUpdate


class CRUDAssetType(CRUDBase[AssetType, AssetCreate, AssetUpdate]):
    pass


asset_type = CRUDAssetType(AssetType)
