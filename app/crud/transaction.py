from typing import List, Union, Dict

from app.crud.base import CRUDBase, multi_query
from app.models import Transaction, Account
from app.schemas import TransactionCreate, TransactionUpdate

from sqlalchemy.orm import Session


class CRUDTransaction(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    def get_multi_by_user(self,
                          db: Session,
                          user_id: int,
                          skip: int = 0,
                          limit: int = 100,
                          as_dict: bool = False) -> Union[List[Transaction], Dict[int, Transaction]]:
        query = db.query(self.model).join(Account).filter(Account.user_id == user_id)
        return multi_query(query, skip=skip, limit=limit, as_dict=as_dict)


transaction = CRUDTransaction(Transaction)
