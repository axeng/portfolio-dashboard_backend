from typing import List

from app import crud, schemas
from app.dependencies.auth import get_user
from app.dependencies.database import get_db
from app.routers import api_router
from app.workers.main import app as celery_app

from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.workers.tasks.external_apis_fetch_data import external_apis_fetch_data

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

app.include_router(api_router)


# TODO delete
@app.get("/secure")
async def secure(user: dict = Depends(get_user)):
    return {"Bravo": "Congrats"}


# TODO delete
@app.get("/user_list", response_model=List[schemas.User])
async def user_list(db: Session = Depends(get_db)):
    users = crud.user.get_multi(db)
    return users


# TODO delete
@app.get("/asset_type_list", response_model=List[schemas.AssetType])
async def asset_type_list(db: Session = Depends(get_db)):
    asset_types = crud.asset_type.get_multi(db)
    return asset_types


# TODO delete
@app.get("/platform_list", response_model=List[schemas.Platform])
async def platform_list(db: Session = Depends(get_db)):
    platforms = crud.platform.get_multi(db)
    return platforms


# TODO delete
@app.get("/transaction_type_list", response_model=List[schemas.TransactionType])
async def transaction_type_list(db: Session = Depends(get_db)):
    transaction_types = crud.transaction_type.get_multi(db)
    return transaction_types


# TODO delete
@app.get("/asset_list", response_model=List[schemas.Asset])
async def asset_list(db: Session = Depends(get_db)):
    assets = crud.asset.get_multi(db)
    return assets


# TODO delete
@app.get("/")
async def root():
    return {"test": "ok"}


# TODO delete
@app.get("/run_task")
async def run_task():
    task = external_apis_fetch_data.delay(None, "transactions")

    return {"task_id": task.task_id}


# TODO delete
@app.get("/task/{task_id}")
async def task_status(task_id):
    res = celery_app.AsyncResult(task_id)
    return {"status": res.ready()}
