from app.crud.commons import CRUDBase
from app.models import Account
from app.schemas import AccountCreate, AccountUpdate


class CRUDAccount(CRUDBase[Account, AccountCreate, AccountUpdate]):
    pass


account = CRUDAccount(Account)
