from typing import Optional
from pydantic import Field
from pydantic import BaseModel, field_validator
from datetime import datetime


class DefaultResponse(BaseModel):
    code: int = 0
    msg: str = "success"


class TaskInfo(BaseModel):
    id: int
    title: str
    level: int
    describe: Optional[str]
    due_date: Optional[datetime]


class SaveTasks(BaseModel):
    title: str = Field(..., min_length=3, max_length=128, description="任务标题")
    level: int = Field(1, ge=1, le=5, description="任务优先级，范围从1到5")
    describe: Optional[str] = Field(None, description="任务描述")
    due_date: Optional[datetime] = Field(None, description="任务截止日期")

    @field_validator('title')
    def validate_title(cls, value: str):
        if not value.strip():
            raise ValueError("标题不能为空")
        return value




