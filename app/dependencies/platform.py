from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from app import crud, models
from app.dependencies.database import get_db


async def get_platform(platform_id: int,
                       db: Session = Depends(get_db)) -> models.Platform:
    platform = crud.platform.get(db, platform_id)

    if platform is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The platform does not exist (id: {platform_id})"
        )

    return platform
