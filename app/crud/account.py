from app.crud.commons import CRUDBase
from app.models import Account
from app.schemas import AccountCreate, AccountUpdate

from sqlalchemy.orm import Session


class CRUDAccount(CRUDBase[Account, AccountCreate, AccountUpdate]):
    def get_multi_by_user(self,
                          db: Session,
                          user_id: int,
                          skip: int = 0,
                          limit: int = 0):
        return db.query(self.model).filter(self.model.user_id == user_id).offset(skip).limit(limit).all()


account = CRUDAccount(Account)
