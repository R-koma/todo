from fastapi import FastAPI
from routes import task as task_router

app = FastAPI()

app.include_router(task_router.router)
