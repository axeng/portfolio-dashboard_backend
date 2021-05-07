from app import models, schemas
from app.crud.commons import CRUDBase


class CRUDTransaction(CRUDBase[models.Transaction, schemas.TransactionCreate, schemas.TransactionUpdate]):
    pass


transaction = CRUDTransaction(models.Transaction)
