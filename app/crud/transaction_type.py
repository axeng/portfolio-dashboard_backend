from typing import Optional, Dict

from app.crud.base import CRUDBase
from app.models import TransactionType
from app.schemas import TransactionTypeCreate, TransactionTypeUpdate

from sqlalchemy.orm import Session


class CRUDTransactionType(CRUDBase[TransactionType, TransactionTypeCreate, TransactionTypeUpdate]):
    def get_by_name(self, db: Session, name: str) -> Optional[TransactionType]:
        return db.query(self.model).filter(self.model.name == name).first()

    def get_dict(self, db: Session) -> Dict[str, int]:
        type_list = db.query(self.model).all()
        type_dict = {}

        for item in type_list:
            type_dict[item.name] = item.id

        return type_dict


transaction_type = CRUDTransactionType(TransactionType)
