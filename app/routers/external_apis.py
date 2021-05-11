from typing import List, Dict, Optional

from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.account import get_account
from app.dependencies.auth import get_user
from app.dependencies.database import get_db, get_read_multi_parameters
from app.dependencies.external_api import get_external_api
from app.schemas import ExternalAPI, ExternalAPICreate, User, ExternalAPIUpdate
from app import crud

router = APIRouter(
    prefix="/external-apis"
)


@router.get("/", response_model=List[ExternalAPI])
async def read_external_apis(account_id: int = None,
                             read_parameters: Dict = Depends(get_read_multi_parameters),
                             db: Session = Depends(get_db),
                             user: User = Depends(get_user)):
    return crud.external_api.get_multi_by_user(db, user.id, account_id, **read_parameters)


@router.post("/", response_model=ExternalAPI)
async def create_external_api(external_api_in: ExternalAPICreate,
                              db: Session = Depends(get_db),
                              user: User = Depends(get_user)):
    account = get_account(external_api_in.account_id, db, user)

    if account.platform_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The account is not linked to any platform"
        )

    return crud.external_api.create(db, external_api_in)


@router.put("/{external_api_id}", response_model=ExternalAPI)
async def update_external_api(external_api_in: ExternalAPIUpdate,
                              external_api: ExternalAPI = Depends(get_external_api),
                              db: Session = Depends(get_db)):
    return crud.external_api.update(db, external_api, external_api_in)


@router.get("/{external_api_id}", response_model=ExternalAPI)
async def read_external_api(external_api: ExternalAPI = Depends(get_external_api)):
    return external_api


@router.delete("/{external_api_id}", response_model=ExternalAPI)
async def delete_external_api(external_api: ExternalAPI = Depends(get_external_api),
                              db: Session = Depends(get_db)):
    return crud.external_api.remove_obj(db, external_api)
