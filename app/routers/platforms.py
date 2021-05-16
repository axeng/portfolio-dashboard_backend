from typing import List, Dict

from fastapi import APIRouter, Depends

from app.dependencies.database import get_db, get_read_multi_parameters
from app.dependencies.platform import get_platform
from app.schemas import Platform
from app import crud

from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/platforms"
)


@router.get("/", response_model=List[Platform])
async def read_platforms(read_parameters: Dict = Depends(get_read_multi_parameters),
                         db: Session = Depends(get_db)):
    return crud.platform.get_multi(db, **read_parameters)


@router.get("/{platform_id}/", response_model=Platform)
async def read_platform(platform: Platform = Depends(get_platform)):
    return platform
