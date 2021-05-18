from typing import Dict, Union, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import get_user
from app.dependencies.database import get_read_multi_parameters_dict, get_db
from app.schemas import User, Transaction
from app import crud

router = APIRouter(
    prefix="/transactions"
)


@router.get("/", response_model=Union[List[Transaction], Dict[str, Transaction]])
async def read_transactions(read_parameters: Dict = Depends(get_read_multi_parameters_dict),
                            db: Session = Depends(get_db),
                            user: User = Depends(get_user)):
    return crud.transaction.get_multi_by_user(db, user.id, **read_parameters)
