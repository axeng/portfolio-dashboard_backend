from app.crud.base import CRUDBase
from app.models import Transaction
from app.schemas import TransactionCreate, TransactionUpdate


class CRUDTransaction(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    pass


transaction = CRUDTransaction(Transaction)
