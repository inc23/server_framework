from copy import deepcopy
from typing import Generator
from .field import Field, IdField


class MetaModel(type):
    classes_dict = dict()

    def __new__(mcs, model_name: str, parents: tuple, attrs: dict):
        fields = dict()
        new_attrs = {'orm_mode': True}
        for parent in parents:
            new_attrs.update(deepcopy(parent.fields))
        new_attrs.update(attrs)
        foreign_keys = dict()
        related_dict = dict()
        model = super(MetaModel, mcs).__new__(mcs, model_name, parents, new_attrs)
        name = attrs['__qualname__'].lower()
        model.model_name = attrs['__qualname__'].lower()
        for k, v in new_attrs.items():
            if isinstance(v, Field):
                fields.update({k: v})
                if v.foreign_key:
                    # foreign_keys.update({k: str(v.foreign_key).split('.')})
                    # v.foreign_key.owner.related_dict.update({v.foreign_key.name: [v.owner.model_name, v.name]})
                    foreign_keys.update({k: v})
                    v.foreign_key.owner.related_dict.update({v.foreign_key.name: v})
        model.fields = fields
        model.foreign_keys = foreign_keys
        model.related_dict = related_dict
        if model.orm_mode:
            mcs.classes_dict.update({name: model})
        return model

    @staticmethod
    def order_by():
        return []

    @property
    def objects(cls):
        from .queryset import QuerySet
        return QuerySet(cls)

    @classmethod
    def create_tables(mcs) -> None:
        CreateTable(mcs.classes_dict)


class CreateTable:

    def __init__(self, classes_dict: dict):
        self.classes_dict = classes_dict
        self._create_tables()

    def _create_tables(self) -> None:
        from .connector import connector
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

    def _create_lines(self, fields: dict) -> str:
        yield ',\r\n\t'.join(self._create_line(fields))
        foreign_key_line = ',\t'.join(self._create_foreign_key_line(fields))
        if foreign_key_line:
            yield foreign_key_line

    @staticmethod
    def _create_line(field: dict) -> Generator[str, None, None]:
        for name, field in field.items():
            line = f'{name} {field.get_line()}'
            yield line

    @staticmethod
    def _create_foreign_key_line(field: dict) -> Generator[str, None, None]:
        for name, field in field.items():
            if field.foreign_key is not None:
                model, foreign_field = str(field.foreign_key).split('.')
                on_delete = field.on_delete if field.on_delete else ''
                yield f'\r\n\tFOREIGN KEY ({model}) REFERENCES {model}({foreign_field}){on_delete}'


class BaseModel(metaclass=MetaModel):

    id = IdField(nullable=True)
    orm_mode = False

    def __init__(self, new_instance: bool = True, **kwargs):
        super(BaseModel, self).__init__()
        self.value_fields_dict = dict()
        self.new_instance = new_instance
        if kwargs:
            for key in self.fields:
                setattr(self, key, kwargs.get(key, None))

    def save(self) -> None:
        self.__class__.objects.save(self.value_fields_dict, self)

    def __eq__(self, other):
        return self.id == other.id
