from app.dependencies.auth import get_user
from app.dependencies.database import get_db
from app.schemas import User, Account
from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session

from app import crud


def get_account(account_id: int,
                db: Session = Depends(get_db),
                user: User = Depends(get_user)) -> Account:
    account = crud.account.get(db, account_id)

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The account does not exist (id: {account_id})"
        )

    if account.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"The account does not belong to the user (id: {account_id})"
        )

    return account
