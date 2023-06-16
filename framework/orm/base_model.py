import os
from typing import Generator
import sqlite3
from field import Field, IdField, FloatField, PasswordField, IntField
from framework.settings import db_dir_path, db_name


class MetaModel(type):
    class_dict = dict()

    def __new__(mcs, model_name: str, parents: tuple, attrs: dict):
        fields = {'id': IdField()}
        for k, v in attrs.items():
            if isinstance(v, Field):
                fields.update({k: v})
        model = super(MetaModel, mcs).__new__(mcs, model_name, parents, attrs)
        name = attrs['__qualname__'].lower()
        setattr(model, 'fields', fields)
        setattr(model, 'model_name', name)
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
        db_path = os.path.join(db_dir_path, db_name)
        conn = sqlite3.connect(db_path)
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
    pass


class OneTable(BaseModel):

    one = FloatField()
    two = IntField()


class TwoTable(BaseModel):
    one = IntField(foreign_key='one_table.id')
    two = FloatField()
    three = IntField(foreign_key='one_table.id')


MetaModel.create_tables()
