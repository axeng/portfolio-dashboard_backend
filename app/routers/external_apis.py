from typing import List, Dict, Union

from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.account import get_account
from app.dependencies.auth import get_user
from app.dependencies.database import get_db, get_read_multi_parameters_dict
from app.dependencies.external_api import get_external_api
from app.platforms import platform_to_module

from app.schemas import ExternalAPI, ExternalAPICreate, User, ExternalAPIUpdate
from app import crud
from app.platforms.commons import DataTypeEnum
from app.workers.tasks.external_apis_fetch_data import external_apis_fetch_data

router = APIRouter(
    prefix="/external-apis"
)


@router.get("/", response_model=Union[List[ExternalAPI], Dict[str, ExternalAPI]])
async def read_external_apis(read_parameters: Dict = Depends(get_read_multi_parameters_dict),
                             db: Session = Depends(get_db),
                             user: User = Depends(get_user)):
    return crud.external_api.get_multi_by_user(db, user.id, **read_parameters)


@router.post("/", response_model=ExternalAPI)
async def create_external_api(external_api_in: ExternalAPICreate,
                              db: Session = Depends(get_db),
                              user: User = Depends(get_user)):
    # Check that the account is owned by the user
    await get_account(external_api_in.account_id, db, user)

    return crud.external_api.create(db, external_api_in)


@router.put("/{external_api_id}/", response_model=ExternalAPI)
async def update_external_api(external_api_in: ExternalAPIUpdate,
                              external_api: ExternalAPI = Depends(get_external_api),
                              db: Session = Depends(get_db)):
    return crud.external_api.update(db, external_api, external_api_in)


@router.get("/{external_api_id}/", response_model=ExternalAPI)
async def read_external_api(external_api: ExternalAPI = Depends(get_external_api)):
    return external_api


@router.delete("/{external_api_id}/", response_model=ExternalAPI)
async def delete_external_api(external_api: ExternalAPI = Depends(get_external_api),
                              db: Session = Depends(get_db)):
    return crud.external_api.remove_obj(db, external_api)


@router.post("/{external_api_id}/fetch-data/{data_type}/")
async def fetch_data(data_type: DataTypeEnum,
                     external_api: ExternalAPI = Depends(get_external_api)):
    platform_module = platform_to_module[external_api.account.platform.name]

    if data_type not in platform_module.supported_data_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The data type is not available for this platform"
        )

    task = external_apis_fetch_data.delay(data_type.value, external_api_id=external_api.id)

    return {"task_id": task.task_id}
