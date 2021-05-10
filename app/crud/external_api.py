from app.crud.commons import CRUDBase
from app.models import ExternalAPI
from app.schemas import ExternalAPICreate, ExternalAPIUpdate


class CRUDExternalAPI(CRUDBase[ExternalAPI, ExternalAPICreate, ExternalAPIUpdate]):
    pass


excternal_api = CRUDExternalAPI(ExternalAPI)
