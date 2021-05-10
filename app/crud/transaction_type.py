from typing import Optional

from app.crud.commons import CRUDBase
from app.models import TransactionType
from app.schemas import TransactionTypeCreate, TransactionTypeUpdate

from sqlalchemy.orm import Session


class CRUDTransactionType(CRUDBase[TransactionType, TransactionTypeCreate, TransactionTypeUpdate]):
    def get_by_name(self, db: Session, name: str) -> Optional[TransactionType]:
        return db.query(TransactionType).filter(TransactionType.name == name).first()


transaction_type = CRUDTransactionType(TransactionType)
