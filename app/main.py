from typing import List

from app import crud
from app.dependencies.auth import get_user
from app.dependencies.database import get_db
from app.routers import api_router
from app.schemas import User, Asset
from app.workers.main import app as celery_app

from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

app = FastAPI()

origins = [
    "http://localhost:8081"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(
    api_router,
    dependencies=[Depends(get_user)]
)


# TODO delete
@app.get("/user_list", response_model=List[User])
async def user_list(db: Session = Depends(get_db)):
    users = crud.user.get_multi(db)
    return users


# TODO delete
@app.get("/asset_list", response_model=List[Asset])
async def asset_list(db: Session = Depends(get_db)):
    assets = crud.asset.get_multi(db)
    return assets


# TODO delete
@app.get("/task/{task_id}")
async def task_status(task_id):
    res = celery_app.AsyncResult(task_id)
    return {"status": res.ready()}
