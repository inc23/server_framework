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

    def __str__(self):
        return f'{self.name} {self.last_name}'


class OneTable(BaseModel):
    one = FloatField(defaults=100000000000)
    two = IntField(nullable=True)
    date = DateField(defaults=datetime.utcnow)


class TwoTable(BaseModel):
    one = IntField(foreign_key='onetable.id')


# MetaModel.create_tables()
#
#
# user = User()
# user.name = 'Ihor'
# user.last_name = 'Petrichenko'
# user.email = 'p@ukr.net'
# user.password = '230588'
# user.is_admin = True
#
# user.save()


# a = OneTable.objects.filter(
#     ((OneTable.one == 20) | (OneTable.one == 200)) | ((OneTable.one == 1110) | (OneTable.one < -100))).all()
# print(a)
#
b = OneTable.objects.get(OneTable.id == 1)
print(b)
#
# a = OneTable.objects.filter(OneTable.two == None).all()
# print(a)
