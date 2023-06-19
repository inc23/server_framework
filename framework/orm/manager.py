from .connector import connector
from .field import Expression
from .query import Query


class Manager:

    def __init__(self, model):
        self.model = model
        self.model_name = model.model_name
        self.fields = model.fields.keys()
        q = Query()
        self.q = q.SELECT(*self.fields).FROM(self.model_name)
        self.conn = connector

    def _fetch(self):
        query = str(self.q)
        db_result = self.conn.fetch(query)
        result = []
        for row in db_result:
            model = self.model(new_instance=False)
            for field, val in zip(self.fields, row):
                setattr(model, field, val)
            result.append(model)
        return result

    def filter(self, expression: Expression = None, **kwargs):
        self.q = self.q.WHERE(expression=expression, **kwargs)
        print(self.q)
        return self

    def all(self):
        return self._fetch()

    def get(self, expression: Expression = None, **kwargs):
        self.filter(expression, **kwargs)
        result = self._fetch()[0]
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
        self.conn.update(query)

    def _new(self, field_dict: dict) -> None:
        q = Query()
        q = q.INSERT(self.model.model_name, *field_dict.keys()).VALUES(*field_dict.values())
        query = str(q)
        self.conn.create(query, *field_dict.values())



