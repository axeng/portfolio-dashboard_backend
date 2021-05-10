from typing import Optional

from app.crud.commons import CRUDBase
from app.models import Platform
from app.schemas import PlatformCreate, PlatformUpdate

from sqlalchemy.orm import Session


class CRUDPlatform(CRUDBase[Platform, PlatformCreate, PlatformUpdate]):
    def get_by_name(self, db: Session, name: str) -> Optional[Platform]:
        return db.query(Platform).filter(Platform.name == name).first()


platform = CRUDPlatform(Platform)
