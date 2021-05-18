from typing import Dict, Union, List

from app.crud.base import CRUDBase, model_list_to_dict
from app.models import Account
from app.schemas import AccountCreate, AccountUpdate

from sqlalchemy.orm import Session


class CRUDAccount(CRUDBase[Account, AccountCreate, AccountUpdate]):
    def get_multi_by_user(self,
                          db: Session,
                          user_id: int,
                          filter_platforms: bool = False,
                          skip: int = 0,
                          limit: int = 100,
                          as_dict: bool = False) -> Union[List[Account], Dict[int, Account]]:
        query = db.query(self.model).filter(self.model.user_id == user_id)

        if filter_platforms:
            query = query.filter(self.model.platform_id != None)

        result = query.offset(skip).limit(limit).all()

        if as_dict:
            return model_list_to_dict(result)
        return result


account = CRUDAccount(Account)
