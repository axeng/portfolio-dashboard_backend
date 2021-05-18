from typing import Union, List, Dict

from app.crud.base import CRUDBase, multi_query
from app.models import ExternalAPI, Account
from app.schemas import ExternalAPICreate, ExternalAPIUpdate

from sqlalchemy.orm import Session


class CRUDExternalAPI(CRUDBase[ExternalAPI, ExternalAPICreate, ExternalAPIUpdate]):
    def get_multi_by_user(self,
                          db: Session,
                          user_id: int,
                          skip: int = 0,
                          limit: int = 100,
                          as_dict: bool = False) -> Union[List[ExternalAPI], Dict[int, ExternalAPI]]:
        query = db.query(self.model).join(Account).filter(Account.user_id == user_id)
        return multi_query(query, skip=skip, limit=limit, as_dict=as_dict)


external_api = CRUDExternalAPI(ExternalAPI)
