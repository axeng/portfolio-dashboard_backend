from typing import List, Dict, Union

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.dependencies.account import get_account
from app.dependencies.auth import get_user
from app.dependencies.database import get_db, get_read_multi_parameters_dict
from app.dependencies.platform import get_platform
from app.schemas import Account, AccountCreate, User, AccountUpdate
from app import crud

router = APIRouter(
    prefix="/accounts"
)


@router.get("/", response_model=Union[List[Account], Dict[str, Account]])
async def read_accounts(filter_platforms: bool = False,
                        read_parameters: Dict = Depends(get_read_multi_parameters_dict),
                        db: Session = Depends(get_db),
                        user: User = Depends(get_user)):
    return crud.account.get_multi_by_user(db, user.id, filter_platforms=filter_platforms, **read_parameters)


@router.post("/", response_model=Account)
async def create_account(account_in: AccountCreate,
                         db: Session = Depends(get_db),
                         user: User = Depends(get_user)):
    if account_in.platform_id is not None:
        await get_platform(account_in.platform_id, db)

    if account_in.parent_account_id is not None:
        await get_account(account_in.parent_account_id, db, user)

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
