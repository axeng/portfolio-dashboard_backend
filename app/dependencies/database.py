from typing import Dict

from app.database import SessionLocal

from fastapi import Depends


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


async def get_read_multi_parameters_dict(read_parameters: Dict = Depends(get_read_multi_parameters),
                                         as_dict: bool = False) -> Dict:
    return {
        **read_parameters,
        "as_dict": as_dict
    }
