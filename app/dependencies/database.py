from typing import Dict

from app.database import SessionLocal
from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.dependencies.auth import get_user


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_read_multi_parameters(skip: int = 0,
                                    limit: int = 100) -> Dict:
    return {
        "skip": skip,
        "limit": limit
    }


def get_account(account_id: int,
                db: Session = Depends(get_db),
                user: schemas.User = Depends(get_user)) -> models.Account:
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


async def get_external_api(external_api_id: int,
                           db: Session = Depends(get_db),
                           user: schemas.User = Depends(get_user)) -> models.ExternalAPI:
    external_api = crud.external_api.get(db, external_api_id)

    if external_api is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The external api does not exist (id: {external_api_id})"
        )

    if external_api.account.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"The external api does not belong to the user (id: {external_api_id})"
        )

    return external_api


async def get_platform(platform_id: int,
                       db: Session = Depends(get_db)) -> models.Platform:
    platform = crud.platform.get(db, platform_id)

    if platform is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The platform does not exist (id: {platform_id})"
        )

    return platform
