from app.crud.commons import CRUDBase
from app.models import TransactionReference
from app.schemas import TransactionReferenceCreate, TransactionReferenceUpdate


class CRUDTransactionReference(CRUDBase[TransactionReference, TransactionReferenceCreate, TransactionReferenceUpdate]):
    pass


transaction_reference = CRUDTransactionReference(TransactionReference)
