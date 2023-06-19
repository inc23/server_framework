from datetime import datetime
from framework.orm.base_model import BaseModel, MetaModel
from framework.orm.field import FloatField, IntField, DateField, TextField, PasswordField, EmailField, BoolField


class User(BaseModel):

    name = TextField(nullable=False)
    last_name = TextField(nullable=False)
    password = PasswordField()
    email = EmailField(nullable=False, unique=True)
    created_at = DateField(defaults=datetime.utcnow)
    is_admin = BoolField()


class OneTable(BaseModel):

    one = FloatField(defaults=100000000000)
    two = IntField(nullable=True)
    date = DateField(defaults=datetime.utcnow)


MetaModel.create_tables()
# class TwoTable(BaseModel):
#     one = IntField(foreign_key='one_table.id')
#     two = FloatField()
#     three = IntField(foreign_key='one_table.id')
#     # time = DateField()
#     # pwd = PasswordField()


# MetaModel.create_tables()
#
# print(OneTable.__dict__)

a = OneTable()
# a.one = 100000
# a.two = 2
a.save()

a = OneTable.objects.filter(
    ((OneTable.one == 50000) & (
        OneTable.two == 200)) | (
            (OneTable.one == 100000) & (
                OneTable.two == 100))).all()
for i in a:
    print(f"{i=}, {i.one=} {i.two=} {i.date=}")

b = OneTable.objects.filter()


