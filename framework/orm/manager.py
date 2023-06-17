from typing import List
from .connector import connector
from .query import Query


class ModelResult:

    def __init__(self, name: str, result_dict: dict):
        self.result_dict = result_dict
        for field, val in result_dict.items():
            setattr(self, field, val)
        self._name = name
        self.__class__.__qualname__ = f'{name.capitalize()}ResultId{self.id}'

    def save(self) -> None:
        set_dict = dict()
        for key in self.result_dict:
            if self.result_dict[key] != getattr(self, key):
                set_dict.update({key: getattr(self, key)})
        q = Query()
        q = q.UPDATE(self._name).SET(
            **set_dict).WHERE(id=self.id)
        query = str(q)
        connector.update(query)


class Manager:

    def __init__(self, model):
        self.model = model
        self.model_name = model.model_name
        self.fields = model.fields.keys()
        q = Query()
        self.q = q.SELECT(*self.fields).FROM(self.model_name)
        self.conn = connector

    def _fetch(self) -> List[ModelResult]:
        query = str(self.q)
        q = Query()
        self.q = q.SELECT(*self.fields).FROM(self.model_name)
        db_result = self.conn.fetch(query)
        result = []
        result_dict = dict()
        for row in db_result:
            for field, val in zip(self.fields, row):
                result_dict.update({field: val})
            result.append(ModelResult(self.model_name, result_dict))
        return result

    def filter(self, **kwargs):
        self.q = self.q.WHERE(**kwargs)
        return self

    def all(self) -> List[ModelResult]:
        return self._fetch()

    def get(self, **kwargs) -> ModelResult:
        self.filter(**kwargs)
        return self._fetch()[0]

    def new(self, *args) -> None:
        q = Query()
        q = q.INSERT(self.model.model_name, *self.fields).VALUES(*args)
        query = str(q)
        self.conn.create(query, *args)



