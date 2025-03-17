from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from crud import tasks
from utils.enums import FieldBy, Order
from utils.schemas import SaveTasks, DefaultResponse, TaskInfo

router = APIRouter()


@router.post('/create', response_model=TaskInfo)
def create_task(request: SaveTasks, db: Session = Depends(get_db)):
    return tasks.create(db=db, obj_in=request)


@router.post('/update', response_model=DefaultResponse)
def create_task(task_id: int, request: SaveTasks, db: Session = Depends(get_db)):
    obj = tasks.get(db=db, _id=task_id)
    if obj is None:
        return DefaultResponse(code='1001', msg="任务不存在")
    try:
        tasks.update(db=db, db_obj=obj, obj_in=request)
        return DefaultResponse(code='0', msg="更新成功")
    except Exception as e:
        return DefaultResponse(code='1002', msg="更新失败")


@router.post('/del', response_model=DefaultResponse)
def create_task(task_id: int, db: Session = Depends(get_db)):
    obj = tasks.get(db=db, _id=task_id)
    if obj is None:
        return DefaultResponse(code='1001', msg="任务不存在")
    try:
        tasks.remove(db=db, _id=task_id)
        return DefaultResponse(code='0', msg="删除成功")
    except Exception as e:
        return DefaultResponse(code='1003', msg="删除失败")


@router.get('/info', response_model=TaskInfo)
def create_task(task_id: int, db: Session = Depends(get_db)):
    return tasks.get(db=db, _id=task_id)


@router.get('/list', response_model=List[TaskInfo])
def create_task(page: int = 1, limit: int = 10, field_by: Optional[FieldBy] = None, order: Order = Order.ASC,
                db: Session = Depends(get_db)):
    return tasks.get_multi(db=db, page=page, limit=limit, field_by=field_by, order=order)
