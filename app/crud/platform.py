from app.crud.commons import CRUDBase
from app.models import Platform
from app.schemas import PlatformCreate, PlatformUpdate


class CRUDPlatform(CRUDBase[Platform, PlatformCreate, PlatformUpdate]):
    pass


platform = CRUDPlatform(Platform)
