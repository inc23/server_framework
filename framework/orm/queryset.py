from typing import Any
from framework import settings
from .connector import connector
from .field import Expression
from .query import Query


class QuerySet:

    def __init__(self, model):
        from .base_model import MetaModel
        self.model: MetaModel = model
        self.model_name = model.model_name
        self.fields = model.fields.keys()
        self._related_data: dict | None = None
        self._conn = connector
        self._expression = None
        self._filter_kwargs = dict()
        self._is_get = False
        self._is_filter = False
        self._select_related_args = None
        self._result = None

    def filter(self, expression: Expression = None, **kwargs):
        if expression:
            if self._expression is None:
                self._expression = expression
            else:
                self._expression &= expression
        self._filter_kwargs.update(kwargs)
        self._is_filter = True
        return self

    def get(self, expression: Expression = None, **kwargs) -> Any:
        self.filter(expression, **kwargs)
        self._is_get = True
        return self

    def select_related(self, *args):
        self._select_related_args = args
        return self

    def _get_select_related_query(self, q: Query, *args: str) -> Query:
        related_data = dict()
        if args:
            for k, v in self.model.related_fields.items():
                if k in args:
                    related_data.update({k: v})
        else:
            related_data = self.model.related_fields
        if related_data:
            related_models = []
            for v in related_data.values():
                related_models.append(f'{v[0]}.*')
            q = q.SELECT(f'{self.model_name}.*', *related_models).FROM(self.model_name)
            for model_field in related_data.items():
                q.JOIN(self.model_name, model_field)
            self._related_data = related_data
        return q

    def _build_query(self):
        q = Query()
        if self._select_related_args is None:
            q = q.SELECT(*self.fields).FROM(self.model_name)
        else:
            q = self._get_select_related_query(q, *self._select_related_args)
        if self._is_filter:
            q = q.WHERE(self._expression, **self._filter_kwargs)
        return str(q)

    def _get_db_result(self) -> list:
        query = self._build_query()
        if settings.echo_sql:
            print(query)
        db_result = self._conn.fetch(query)
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
                    from .base_model import MetaModel
                    model_rel = MetaModel.classes_dict[v[0]](new_instance=False)
                    for field, val in zip(model_rel.fields, row):
                        setattr(model_rel, field, val)
                    setattr(model, k, model_rel)
                    row = row[len(model_rel.fields):]
            result.append(model)
        self._related_data = None
        return result

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

    def __iter__(self):
        if self._result is None:
            self._result = self._fetch()
        return iter(self._result)

    def __getattr__(self, item):
        if self._result is None:
            self._result = self._fetch()[0]
        return getattr(self._result, item)

    def __bool__(self):
        if self._result is None:
            self._result = self._fetch()
        return bool(self._result)



# class QuerySet:
#     def __init__(self, model: MetaModel):
#         self.model = model
#         self.model_name = model.model_name
#         self.fields = model.fields.keys()
#         self._q = None
#         self._conn = connector
#         self._related_data: dict | None = None
#         self._set_default_q()
#
#     def _set_default_q(self):
#         q = Query()
#         self._q = q.SELECT(*self.fields).FROM(self.model_name)
#
#     def _get_db_result(self) -> list:
#         query = str(self._q)
#         if settings.echo_sql:
#             print(self._q)
#         db_result = self._conn.fetch(query)
#         self._set_default_q()
#         return db_result
#
#     def _fetch(self) -> list:
#         result = []
#         for row in self._get_db_result():
#             model = self.model(new_instance=False)
#             for field, val in zip(self.fields, row):
#                 setattr(model, field, val)
#             if self._related_data:
#                 row = row[len(model.fields):]
#                 for k, v in self._related_data.items():
#                     model_rel = MetaModel.classes_dict[v[0]](new_instance=False)
#                     for field, val in zip(model_rel.fields, row):
#                         setattr(model_rel, field, val)
#                     setattr(model, k, model_rel)
#                     row = row[len(model_rel.fields):]
#             result.append(model)
#         self._related_data = None
#         return result
#
#     def filter(self, expression: Expression = None, **kwargs):
#         print(expression)
#         self._q = self._q.WHERE(expression=expression, **kwargs)
#         return self
#
#     def all(self) -> list:
#         return self._fetch()
#
#     def get(self, expression: Expression = None, **kwargs) -> Any:
#         self.filter(expression, **kwargs)
#         result = self._fetch()
#         if not result:
#             return None
#         return result[0]
#
#     def save(self, fields_dict: dict = None, instance=None, ) -> None:
#         for key in self.model.fields:
#             getattr(instance, key)
#         if instance.new_instance:
#             self._new(fields_dict)
#         else:
#             self._update(instance)
#
#     def _update(self, instance) -> None:
#         q = Query()
#         q = q.UPDATE(self.model_name).SET(
#             **instance.value_fields_dict).WHERE(id=instance.id)
#         query = str(q)
#         self._conn.update(query)
#
#     def _new(self, field_dict: dict) -> None:
#         q = Query()
#         q = q.INSERT(self.model.model_name, *field_dict.keys()).VALUES(*field_dict.values())
#         query = str(q)
#         self._conn.create(query, *field_dict.values())
#
#     def select_related(self, *args: str):
#         related_data = dict()
#         if args:
#             for k, v in self.model.related_fields.items():
#                 if k in args:
#                     related_data.update({k: v})
#         else:
#             related_data = self.model.related_fields
#         if related_data:
#             related_models = []
#             for v in related_data.values():
#                 related_models.append(f'{v[0]}.*')
#             q = Query()
#             self._q = q.SELECT(f'{self.model_name}.*', *related_models).FROM(self.model_name)
#             for model_field in related_data.items():
#                 self._q.JOIN(self.model_name, model_field)
#             self._related_data = related_data
#         return self
