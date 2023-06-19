from typing import Generator
from .field import FieldBase, IdField
from .connector import connector
from .manager import Manager


class MetaModel(type):
    class_dict = dict()

    def __new__(mcs, model_name: str, parents: tuple, attrs: dict):
        fields = dict()
        new_attrs = {'id': IdField(nullable=True)}
        new_attrs.update(attrs)
        for k, v in new_attrs.items():
            if isinstance(v, FieldBase):
                fields.update({k: v})
        model = super(MetaModel, mcs).__new__(mcs, model_name, parents, new_attrs)
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
            print(query)
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
            line = f'{name} {field.get_line()}'
            yield line

    @staticmethod
    def _create_foreign_key_line(field: dict) -> Generator:
        for name, field in field.items():
            if field.foreign_key is not None:
                yield f'\r\n\tFOREIGN KEY ({name}) REFERENCES {field.foreign_key}'


class BaseModel(metaclass=MetaModel):

    def __init__(self, new_instance: bool = True, **kwargs):
        super(BaseModel, self).__init__()
        self.value_fields_dict = dict()
        self.new_instance = new_instance
        if kwargs:
            for key in self.fields:
                setattr(self, key, kwargs.get(key, None))

    def save(self):
        self.objects.save(self.value_fields_dict, self)
