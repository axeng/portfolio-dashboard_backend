from typing import Dict

from app.database import SessionLocal


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
