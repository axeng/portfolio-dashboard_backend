from app.external_apis import kraken
from app.workers.main import app as celery_app

from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware

from app.auth import get_current_user
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


# TODO delete
@app.get("/secure")
async def secure(current_user: dict = Depends(get_current_user)):
    print(current_user)
    return {"Bravo": "Congrats"}


# TODO delete
@app.get("/")
def root():
    task = external_apis_fetch_data.delay(None, "transactions")

    return {"task_id": task.task_id}


# TODO delete
@app.get("/task/{task_id}")
def task_status(task_id):
    res = celery_app.AsyncResult(task_id)
    return {"status": res.ready()}
