from typing import Union, List, Dict

from app.crud.base import CRUDBase, model_list_to_dict
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
        result = db.query(self.model).join(Account).filter(Account.user_id == user_id).offset(skip).limit(limit).all()

        if as_dict:
            return model_list_to_dict(result)
        return result


external_api = CRUDExternalAPI(ExternalAPI)
