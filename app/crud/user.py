from typing import Optional

from app.crud.commons import CRUDBase
from app.models import User
from app.schemas import UserCreate, UserUpdate

from sqlalchemy.orm import Session


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_keycloak_user_id(self, db: Session, keycloak_user_id: str) -> Optional[User]:
        return db.query(User).filter(User.keycloak_user_id == keycloak_user_id).first()


user = CRUDUser(User)
