from copy import copy
from datetime import datetime

from framework.orm.query import Query
from .connector import DBConnector
from .model_list import ModelList, StrId


class Manager:

    def __init__(self, model):
        self.item_dict = None
        self.get_object = False
        self.fields_only = None
        self.update_dict = dict()
        self.fields = model.fields.keys()
        self.conn = DBConnector()
        self.model = model
        q = Query()
        self.q = q.SELECT(*self.fields).FROM(self.model.model_name)

    def only(self, *fields):
        self.fields_only = fields
        q = Query()
        self.q = q.SELECT(*fields).FROM(self.model.model_name)
        return self

    def distinct(self):
        q = Query()
        fields = self._get_fields()
        self.q = q.SELECTD(*fields,).FROM(self.model.model_name)
        return self

    def all(self):
        self.fields_only = None
        q = Query()
        self.q = q.SELECT(*self.fields).FROM(self.model.model_name)
        return self

    def _get_fields(self):
        if self.fields_only is not None:
            return self.fields_only
        return self.fields

    def _fetch(self):
        q = str(self.q)
        db_result = self.conn.fetch(q)
        result = ModelList(model=self.model, get_flag=self.get_object)
        fields = self._get_fields()
        for row in db_result:
            model = self.model()
            res_dict = dict()
            for field, val in zip(fields, row):
                setattr(model, field, val)
                res_dict.update({field: val})
            result.append(res_dict)
        return result

    def models(self):
        q = str(self.q)
        db_result = self.conn.fetch(q)
        result = []
        fields = self._get_fields()
        for row in db_result:
            model = self.model()
            for field, val in zip(fields, row):
                setattr(model, field, val)
            result.append(model)
        return result

    def model_str(self):
        q = str(self.q)
        db_result = self.conn.fetch(q)
        result = []
        fields = self._get_fields()
        for row in db_result:
            model = self.model()
            for field, val in zip(fields, row):
                setattr(model, field, val)
            result.append(StrId(model))
        return result

    def values(self):
        return self._fetch()

    def filter(self, **kwargs):
        data = dict()
        for k, v in kwargs.items():
            if isinstance(v, datetime):
                data[k] = f"\'{v.timestamp()}\'"
            elif isinstance(v, tuple) or v is None:
                data[k] = v
            else:
                data[k] = f"\'{v}\'"
        self.q = self.q.WHERE(**data)
        return self

    def new(self, *args):
        q = Query()
        q = q.INSERT(self.model.model_name, *self.fields).VALUES(*args)
        query = str(q)
        self.conn.create(query, *args)

    def save(self, field_dict=None):
        self.fields = self.model.fields.keys()
        if self.item_dict is None:
            field_dict_sort = dict()
            for k in self.fields:
                if k != 'id':
                    field_dict_sort[k] = field_dict[k]
            self.new(*field_dict_sort.values())
        else:
            self.update(self.update_dict)
            self.update_dict.clear()

    def update(self, field_dict):
        q = Query()
        q = q.UPDATE(self.model.model_name).SET(
            **field_dict).WHERE(**self.item_dict)
        query = str(q)
        self.conn.update(query)

    def delete(self):
        if self.get_object:
            q = Query()
            q = q.DELETE(self.model.model_name).WHERE(**self.item_dict)
            query = str(q)
            self.conn.update(query)

    def get(self, id):
        m = Manager(self.model)
        m.item_dict = {'id': id}
        m.get_object = True
        m.q.WHERE(**m.item_dict)
        return m

    def __setattr__(self, key, value):

        if hasattr(self, 'fields') and key in self.fields:
            if key != 'id':
                self.update_dict.update({key: value})
        else:
            super(Manager, self).__setattr__(key, value)

