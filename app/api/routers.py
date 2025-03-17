from fastapi import APIRouter, Depends

from api.v1 import tasks


api_router = APIRouter()

api_router.include_router(tasks.router, prefix="/v1/tasks", tags=["Tasks"])