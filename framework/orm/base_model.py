import os
from typing import Generator
import sqlite3
from field import Field, IdField, FloatField, PasswordField, IntField


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
    def create_tables(mcs) -> None:
        path = os.path.dirname(os.path.abspath(__file__))
        bd_path = os.path.join(path, 'db.db')
        conn = sqlite3.connect(bd_path)
        cursor = conn.cursor()
        for query in mcs._create_query():
            print(query)
            cursor.execute(query)
            conn.commit()

    @classmethod
    def _create_query(mcs) -> list:
        query_list = []
        for model, fields in mcs.class_dict.items():
            query = f'CREATE TABLE IF NOT EXISTS {model} (\r\n\t'
            query += f"{','.join(mcs._create_lines(fields))}\r\n\t"
            query = f'{query[:-1]});'
            query_list.append(query)
        return query_list

    @classmethod
    def _create_lines(mcs, fields: dict) -> Generator:
        yield ',\r\n\t'.join(mcs._create_line(fields))
        foreign_key_line = ',\t'.join(mcs._create_foreign_key_line(fields))
        if foreign_key_line:
            yield foreign_key_line

    @classmethod
    def _create_line(mcs, field: dict) -> Generator:
        for name, field in field.items():
            line = f'{name} {field.type}'
            yield line

    @classmethod
    def _create_foreign_key_line(mcs, field: dict) -> Generator:
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
