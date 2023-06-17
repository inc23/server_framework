from typing import Generator
from .field import Field, IdField
from .connector import connector
from .manager import Manager


class MetaModel(type):
    class_dict = dict()

    def __new__(mcs, model_name: str, parents: tuple, attrs: dict):
        fields = {'id': IdField()}
        new_attr = dict()
        for k, v in attrs.items():
            if isinstance(v, Field):
                fields.update({k: v})
            else:
                new_attr.update({k: v})
        model = super(MetaModel, mcs).__new__(mcs, model_name, parents, attrs)
        name = attrs['__qualname__'].lower()
        model.fields = fields
        model.model_name = attrs['__qualname__'].lower()
        model.objects = Manager(model)
        if name != 'basemodel':
            mcs.class_dict.update({name: fields})
        return model

    @classmethod
    def create_tables(mcs):
        CreateTable(mcs.class_dict)


class CreateTable:

    def __init__(self, classes_dict: dict):
        self.classes_dict = classes_dict
        self._create_tables()

    def _create_tables(self) -> None:
        conn = connector.get_connector()
        cursor = conn.cursor()
        for query in self._create_query():
            cursor.execute(query)
            conn.commit()

    def _create_query(self) -> list:
        query_list = []
        for model, fields in self.classes_dict.items():
            query = f'CREATE TABLE IF NOT EXISTS {model} (\r\n\t'
            query += f"{','.join(self._create_lines(fields))}\r\n\t);"
            query_list.append(query)
        return query_list

    def _create_lines(self, fields: dict) -> Generator:
        yield ',\r\n\t'.join(self._create_line(fields))
        foreign_key_line = ',\t'.join(self._create_foreign_key_line(fields))
        if foreign_key_line:
            yield foreign_key_line

    @staticmethod
    def _create_line(field: dict) -> Generator:
        for name, field in field.items():
            line = f'{name} {field.type}'
            yield line

    @staticmethod
    def _create_foreign_key_line(field: dict) -> Generator:
        for name, field in field.items():
            if field.foreign_key is not None:
                yield f'\r\n\tFOREIGN KEY ({name}) REFERENCES {field.foreign_key}'


class BaseModel(metaclass=MetaModel):

    def __init__(self, **kwargs):
        super(BaseModel, self).__init__()
        self.new_model_instance_fields_dict = dict()
        if kwargs:
            for key in self.fields:
                if key != 'id':
                    setattr(self, key, kwargs.get(key, None))

    def save(self):
        self.objects.new(*self.new_model_instance_fields_dict.values())



