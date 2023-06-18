from datetime import datetime
from framework.orm.base_model import BaseModel, MetaModel
from framework.orm.field import FloatField, IntField, DateField, PasswordField, TextField, ImageField
from orm.security import verify_password


class OneTable(BaseModel):

    one = FloatField()
    two = IntField(nullable=True)
    date = DateField(defaults=datetime.utcnow)


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
a.one = 100000
# a.two = 2
a.save()
print(
    type(
        ((OneTable.one == 1) & (
            OneTable.two == 2)) | (
                (OneTable.one == 1) & (
                    OneTable.two == 2))))

a = OneTable.objects.filter(
    ((OneTable.one == 50000) & (
        OneTable.two == 200)) | (
            (OneTable.one == 100000) & (
                OneTable.two == 100))).all()
for i in a:
    print(f"{i=}, {i.one=} {i.two=}")

a = OneTable.one == 1
b = OneTable.two == 2
# print(type(a))


class A:

    def __and__(self, other):
        return f'and  {other}'


a = A()

print(a & 'h')
