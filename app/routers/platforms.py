from typing import List, Dict, Union

from fastapi import APIRouter, Depends

from app.dependencies.database import get_db, get_read_multi_parameters, get_read_multi_parameters_dict
from app.dependencies.platform import get_platform
from app.platforms.commons import get_platform_module
from app.schemas import Platform, PlatformInDB
from app import crud

from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/platforms"
)


@router.get("/", response_model=Union[List[Platform], Dict[str, Platform]])
async def read_platforms(read_parameters: Dict = Depends(get_read_multi_parameters_dict),
                         db: Session = Depends(get_db)):
    return crud.platform.get_multi(db, **read_parameters)


@router.get("/schemas/additional-data/", response_model=Dict[str, Dict])
async def read_additional_data_schemas(read_parameters: Dict = Depends(get_read_multi_parameters),
                                       db: Session = Depends(get_db)):
    platform_list = crud.platform.get_multi(db, **read_parameters)
    platform_schemas = {}

    for platform in platform_list:
        platform_schemas[platform.id] = get_platform_module(platform.name).AdditionalData.schema()

    return platform_schemas


@router.get("/schemas/authentication-data/", response_model=Dict[str, Dict])
async def read_authentication_data_schemas(read_parameters: Dict = Depends(get_read_multi_parameters),
                                           db: Session = Depends(get_db)):
    platform_list = crud.platform.get_multi(db, **read_parameters)
    platform_schemas = {}

    for platform in platform_list:
        platform_schemas[platform.id] = get_platform_module(platform.name).AuthenticationData.schema()

    return platform_schemas


@router.get("/{platform_id}/", response_model=Platform)
async def read_platform(platform: Platform = Depends(get_platform)):
    return platform


@router.get("/{platform_id}/schemas/additional-data/", response_model=Dict)
async def read_additional_data_schema(platform: PlatformInDB = Depends(get_platform)):
    return get_platform_module(platform.name).AdditionalData.schema()


@router.get("/{platform_id}/schemas/authentication-data/", response_model=Dict)
async def read_authentication_data_schema(platform: PlatformInDB = Depends(get_platform)):
    return get_platform_module(platform.name).AuthenticationData.schema()
