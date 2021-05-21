from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, Query

from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


def model_list_to_dict(model_list: List[ModelType]) -> Dict[int, ModelType]:
    model_dict = {}

    for model in model_list:
        model_dict[model.id] = model

    return model_dict


def multi_query(query,
                skip: int = 0,
                limit: int = 100,
                as_dict: bool = False) -> Union[List[ModelType], Dict[int, ModelType]]:
    query = query.offset(skip)
    if limit >= 0:
        query = query.limit(limit)

    result = query.all()

    if as_dict:
        return model_list_to_dict(result)
    return result


# Source: https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app/crud/base.py
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self,
                  db: Session,
                  skip: int = 0,
                  limit: int = 100,
                  as_dict: bool = False) -> Union[List[ModelType], Dict[int, ModelType]]:
        query = db.query(self.model)
        return multi_query(query, skip=skip, limit=limit, as_dict=as_dict)

    def create(self,
               db: Session,
               obj_in: CreateSchemaType,
               **kwargs) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, **kwargs)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self,
               db: Session,
               db_obj: ModelType,
               obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
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

    def remove(self, db: Session, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        return self.remove_obj(db, obj)

    def remove_obj(self, db: Session, obj: ModelType) -> ModelType:
        db.delete(obj)
        db.commit()
        return obj
