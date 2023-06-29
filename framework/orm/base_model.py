from typing import Generator
from .field import Field, IdField
from .connector import connector


class MetaModel(type):
    classes_dict = dict()

    def __new__(mcs, model_name: str, parents: tuple, attrs: dict):
        fields = dict()
        new_attrs = {'id': IdField(nullable=True)}
        new_attrs.update(attrs)
        related_fields = dict()
        for k, v in new_attrs.items():
            if isinstance(v, Field):
                fields.update({k: v})
                if v.foreign_key:
                    related_fields.update({k: v.foreign_key.split('.')})
        model = super(MetaModel, mcs).__new__(mcs, model_name, parents, new_attrs)
        name = attrs['__qualname__'].lower()
        model.fields = fields
        model.model_name = attrs['__qualname__'].lower()
        model.related_fields = related_fields
        from .manager import Manager
        model.objects = Manager(model)
        if name != 'basemodel':
            mcs.classes_dict.update({name: model})
        return model

    @classmethod
    def create_tables(mcs):
        CreateTable(mcs.classes_dict)


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
        for name, model in self.classes_dict.items():
            query = f'CREATE TABLE IF NOT EXISTS {name} (\r\n\t'
            query += f"{','.join(self._create_lines(model.fields))}\r\n\t);"
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
                model, field = field.foreign_key.split('.')
                yield f'\r\n\tFOREIGN KEY ({model}) REFERENCES {model}({field})'


class BaseModel(metaclass=MetaModel):

    id = None

    def __init__(self, new_instance: bool = True, **kwargs):
        super(BaseModel, self).__init__()
        self.value_fields_dict = dict()
        self.new_instance = new_instance
        if kwargs:
            for key in self.fields:
                setattr(self, key, kwargs.get(key, None))

    def save(self) -> None:
        self.objects.save(self.value_fields_dict, self)
