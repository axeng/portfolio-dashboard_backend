from app.crud.commons import CRUDBase
from app.models import ExternalAPI
from app.schemas import ExternalAPICreate, ExternalAPIUpdate

from sqlalchemy.orm import Session


class CRUDExternalAPI(CRUDBase[ExternalAPI, ExternalAPICreate, ExternalAPIUpdate]):
    def get_multi_by_user(self,
                          db: Session,
                          user_id: int,
                          account_id: int = None,
                          skip: int = 0,
                          limit: int = 100):
        query = db.query(self.model).filter(self.model.account.user_id == user_id)

        if account_id is not None:
            query = query.filter(self.model.account_id == account_id)

        return query.offset(skip).limit(limit).all()


external_api = CRUDExternalAPI(ExternalAPI)
