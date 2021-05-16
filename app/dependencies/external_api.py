from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from app import crud, models, schemas
from app.dependencies.auth import get_user
from app.dependencies.database import get_db


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
