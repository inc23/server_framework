from typing import Any
import settings
from .connector import connector
from .field import Expression
from .query import Query


class QuerySet:

    def __init__(self, model):
        from .base_model import MetaModel
        self.model: MetaModel = model
        self.model_name = model.model_name
        self.fields = model.fields.keys()
        self.value_fields_dict = dict()
        self._related_data = dict()
        self._conn = connector
        self._expression = None
        self._filter_kwargs = dict()
        self._is_get = False
        self._is_filter = False
        self._select_related_args = None
        self._result = None
        self._order_by_data = None
        self._limit = None
        self._offset = None

    def limit(self, limit: int):
        self._limit = limit
        return self

    def offset(self, offset: int):
        self._offset = offset
        return self

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

    def order_by(self, *args):
        self._order_by_data = args
        return self

    def _prepare_related_data(self, *args) -> dict:
        related_data = []
        if args:
            for k, v in self.model.foreign_keys.items():
                if k in args:
                    related_data.append((k, str(v.foreign_key).split('.')))
                    self._related_data.update({k: str(v.foreign_key).split('.')})
            for k, v in self.model.related_list:
                if v.owner.model_name in args:
                    related_data.append((k, [v.owner.model_name, v.name]))
                    self._related_data.update(
                        {v.owner.model_name: [v.owner.model_name, v.name]})
        else:
            related_data = {k: str(v.foreign_key).split('.') for k, v in self.model.foreign_keys.items()}
            related_data.update({k: [v.owner.model_name, v.name] for k, v in self.model.related_list})
            self._related_data = {k: str(v.foreign_key).split('.') for k, v in self.model.foreign_keys.items()}
            self._related_data.update(
                {v.owner.model_name: [v.owner.model_name, v.name] for k, v in self.model.related_list})
        return related_data

    def _get_select_related_query(self, q: Query, *args: str) -> Query:
        related_data = self._prepare_related_data(*args)
        if related_data:
            related_models = []
            for k, v in related_data:
                related_models.append(f'{v[0]}.*')
            q = q.SELECT(f'{self.model_name}.*', *related_models).FROM(self.model_name)
            for model_field in related_data:
                q.JOIN(self.model_name, model_field)
        return q

    def _build_query(self) -> str:
        q = Query()
        if self._select_related_args is None:
            q = q.SELECT(*self.fields).FROM(self.model_name)
        else:
            q = self._get_select_related_query(q, *self._select_related_args)
        if self._is_filter:
            q = q.WHERE(self._expression, **self._filter_kwargs)
        order_data = self._order_by_data if self._order_by_data else self.model.order_by()
        if order_data:
            order_data = [str(item) for item in order_data]
            q = q.ORDER_BY(*order_data)
        if self._limit:
            q = q.LIMIT(self._limit)
        if self._offset:
            q = q.OFFSET(self._offset)
        return str(q)

    def _get_db_result(self) -> list:
        query = self._build_query()
        if settings.echo_sql:
            print(query)
        db_result = self._conn.fetch(query)
        return db_result

    @staticmethod
    def _create_model(model_class, fields, row):
        model = model_class(new_instance=False)
        for field, val in zip(fields, row):
            setattr(model, field, val)
        return model

    def _fetch(self) -> list:
        result_dict = dict()
        for row in self._get_db_result():
            model = self._create_model(self.model, self.fields, row)
            model = result_dict.get(model.id, model)
            if self._related_data:
                row = row[len(model.fields):]
                for k, v in self._related_data.items():
                    from .base_model import MetaModel
                    model_rel_class = MetaModel.classes_dict[v[0]]
                    model_rel = self._create_model(model_rel_class, model_rel_class.fields, row)
                    if k not in self.fields:
                        if not getattr(model, k, None):
                            setattr(model, k, [model_rel])
                        elif isinstance(getattr(model, k), list):
                            if model_rel not in getattr(model, k):
                                getattr(model, k).append(model_rel)
                    else:
                        setattr(model, k, model_rel)
                    row = row[len(model_rel.fields):]
            result_dict.update({model.id: model})
        result = list(result_dict.values())
        self._related_data.clear()
        return result[0] if self._is_get and result else result

    def save(self, fields_dict: dict = None, instance=None, ) -> None:
        if instance:
            for key in self.model.fields:
                getattr(instance, key)
            self._new(fields_dict)
        else:
            self._update()

    def _update(self) -> None:
        q = Query()
        q = q.UPDATE(self.model_name).SET(
            **self.value_fields_dict).WHERE(self._expression, **self._filter_kwargs)
        query = str(q)
        from .signal import pre_update, post_update
        pre_update.send(self)
        self._conn.update(query)
        self._result = None
        post_update.send(self)

    def _new(self, field_dict: dict) -> None:
        q = Query()
        q = q.INSERT(self.model.model_name, *field_dict.keys()).VALUES(*field_dict.values())
        query = str(q)
        self._conn.create(query, *field_dict.values())

    def delete(self) -> None:
        if self._is_get:
            q = Query()
            q = q.DELETE(self.model.model_name).WHERE(self._expression, **self._filter_kwargs)
            query = str(q)
            from .signal import delete
            delete.send(self)
            self._conn.update(query)

    def __iter__(self):
        if self._result is None:
            self._result = self._fetch()
        return iter(self._result)

    def __getattr__(self, item):
        if self._result is None:
            self._result = self._fetch()
            if not self._result:
                return []
        return getattr(self._result, item)

    def __bool__(self):
        if self._result is None:
            self._result = self._fetch()
        return bool(self._result)

    def __setattr__(self, key, value):
        if 'fields' in self.__dict__ and key in self.fields:
            self.value_fields_dict[key] = value
        else:
            super(QuerySet, self).__setattr__(key, value)

    def __str__(self):
        if self._is_get:
            if self._result is None:
                self._result = self._fetch()
            return str(self._result)
        else:
            return super(QuerySet, self).__str__()
