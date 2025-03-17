from datetime import datetime
from sqlalchemy import String, Integer, Text, DateTime
from sqlalchemy.orm import  Mapped, mapped_column

from models.base_model import BaseModel


class Tasks(BaseModel):
    __tablename__ = 'tasks'

    title: Mapped[str] = mapped_column(String(128))
    describe: Mapped[str] = mapped_column(Text)
    level: Mapped[int] = mapped_column(Integer, default=1)
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)




