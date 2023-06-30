from typing import Any
from framework import settings
from .connector import connector
from .field import Expression
from .query import Query
from .base_model import MetaModel


class Manager:
    def __init__(self, model: MetaModel):
        self.model = model
        self.model_name = model.model_name
        self.fields = model.fields.keys()
        self._q = None
        self._conn = connector
        self._related_data: dict | None = None
        self._set_default_q()

    def _set_default_q(self):
        q = Query()
        self._q = q.SELECT(*self.fields).FROM(self.model_name)

    def _get_db_result(self) -> list:
        query = str(self._q)
        if settings.echo_sql:
            print(self._q)
        db_result = self._conn.fetch(query)
        self._set_default_q()
        return db_result

    def _fetch(self) -> list:
        result = []
        for row in self._get_db_result():
            model = self.model(new_instance=False)
            for field, val in zip(self.fields, row):
                setattr(model, field, val)
            if self._related_data:
                row = row[len(model.fields):]
                for k, v in self._related_data.items():
                    model_rel = MetaModel.classes_dict[v[0]](new_instance=False)
                    for field, val in zip(model_rel.fields, row):
                        setattr(model_rel, field, val)
                    setattr(model, k, model_rel)
                    row = row[len(model_rel.fields):]
            result.append(model)
        self._related_data = None
        return result

    def filter(self, expression: Expression = None, **kwargs):
        self._q = self._q.WHERE(expression=expression, **kwargs)
        return self

    def all(self) -> list:
        return self._fetch()

    def get(self, expression: Expression = None, **kwargs) -> Any:
        self.filter(expression, **kwargs)
        result = self._fetch()
        if not result:
            return None
        return result[0]

    def save(self, fields_dict: dict = None, instance=None, ) -> None:
        for key in self.model.fields:
            getattr(instance, key)
        if instance.new_instance:
            self._new(fields_dict)
        else:
            self._update(instance)

    def _update(self, instance) -> None:
        q = Query()
        q = q.UPDATE(self.model_name).SET(
            **instance.value_fields_dict).WHERE(id=instance.id)
        query = str(q)
        self._conn.update(query)

    def _new(self, field_dict: dict) -> None:
        q = Query()
        q = q.INSERT(self.model.model_name, *field_dict.keys()).VALUES(*field_dict.values())
        query = str(q)
        self._conn.create(query, *field_dict.values())

    def select_related(self, *args: str):
        related_data = dict()
        if args:
            for k, v in self.model.related_fields.items():
                if k in args:
                    related_data.update({k: v})
        else:
            related_data = self.model.related_fields
        related_models = []
        for v in related_data.values():
            related_models.append(f'{v[0]}.*')
        q = Query()
        self._q = q.SELECT(f'{self.model_name}.*', *related_models).FROM(self.model_name)
        for model_field in related_data.items():
            self._q.JOIN(self.model_name, model_field)
        self._related_data = related_data
        return self
