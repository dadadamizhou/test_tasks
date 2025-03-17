from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models import base_model
from utils.enums import Order, FieldBy

ModelType = TypeVar("ModelType", bound=base_model.BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):

        self.model = model

    def get(self, db: Session, _id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == _id).first()

    def first(self, db: Session, **kwargs) -> Optional[ModelType]:
        query = db.query(self.model)
        for field, value in kwargs.items():
            if hasattr(self.model, field):
                query = query.filter(getattr(self.model, field) == value)
        return query.first()

    def get_multi(
        self, db: Session, *, page: int = 1, limit: int = 100,
        field_by: Optional[FieldBy] = None, order: Order = Order.ASC
    ) -> List[ModelType]:
        page = 1 if page < 1 else page
        query = db.query(self.model)
        if field_by:
            query = query.order_by(getattr(self.model, field_by).asc() if order == Order.ASC else getattr(self.model, field_by).desc())
        return query.offset(page * limit - limit).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, _id: int) -> ModelType:
        obj = db.query(self.model).get(_id)
        db.delete(obj)
        db.commit()
        return obj
