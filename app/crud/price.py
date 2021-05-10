from app.crud.commons import CRUDBase
from app.models import Price
from app.schemas import PriceCreate, PriceUpdate


class CRUDPrice(CRUDBase[Price, PriceCreate, PriceUpdate]):
    pass


price = CRUDPrice(Price)
