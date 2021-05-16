from typing import List, Dict

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.dependencies.account import get_account
from app.dependencies.auth import get_user
from app.dependencies.database import get_db, get_read_multi_parameters
from app.schemas import Account, AccountCreate, User, AccountUpdate
from app import crud

router = APIRouter(
    prefix="/accounts"
)


@router.get("/", response_model=List[Account])
async def read_accounts(read_parameters: Dict = Depends(get_read_multi_parameters),
                        db: Session = Depends(get_db),
                        user: User = Depends(get_user)):
    return crud.account.get_multi_by_user(db, user.id, **read_parameters)


@router.post("/", response_model=Account)
async def create_account(account_in: AccountCreate,
                         db: Session = Depends(get_db),
                         user: User = Depends(get_user)):
    if account_in.parent_account_id is not None:
        get_account(account_in.parent_account_id, db, user)

    return crud.account.create(db, account_in, user_id=user.id)


@router.put("/{account_id}/", response_model=Account)
async def update_account(account_in: AccountUpdate,
                         account: Account = Depends(get_account),
                         db: Session = Depends(get_db)):
    return crud.account.update(db, account, account_in)


@router.get("/{account_id}/", response_model=Account)
async def read_account(account: Account = Depends(get_account)):
    return account


@router.delete("/{account_id}/", response_model=Account)
async def delete_account(account: Account = Depends(get_account),
                         db: Session = Depends(get_db)):
    return crud.account.remove_obj(db, account)
