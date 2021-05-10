from app.crud.commons import CRUDBase
from app.models import Asset
from app.schemas import AssetCreate, AssetUpdate


class CRUDAsset(CRUDBase[Asset, AssetCreate, AssetUpdate]):
    pass


asset = CRUDAsset(Asset)
