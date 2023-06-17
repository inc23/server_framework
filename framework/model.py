from datetime import datetime
from framework.orm.base_model import BaseModel
from framework.orm.field import FloatField, IntField, DateField, PasswordField, TextField, ImageField
from orm.security import verify_password


class OneTable(BaseModel):

    one = FloatField()
    two = IntField()


class TwoTable(BaseModel):
    one = IntField(foreign_key='one_table.id')
    two = FloatField()
    three = IntField(foreign_key='one_table.id')
    # time = DateField()
    # pwd = PasswordField()

#
# a = TwoTable()
# a.time = datetime.utcnow()
# a.two = 142
# a.three = 15
# a.pwd = '2305888'
# # print(a.time)
# # print(verify_password('2305888', a.pwd))
# # print(a.fields_dict)
# # print(TwoTable())
# a = OneTable.objects.get(id=1)
# print(a.one)
# a.one = 2
# a.two = 7
# a.save()
# print(a.one)
#
a = OneTable.objects.get(id=1)
print(a.one)
print(a.__dict__)
a.one = 1
print(a.one)
print(a.__dict__)
#
# b = OneTable.objects.all()
#
#
# c = OneTable.objects.filter(one=2).filter(id=3).all()
# print(c)
# # class A:
#     pass
#
# a = A()
# a.__qualname__ = 'hello'
# print(a)


# a = OneTable(one=1, two=100)
# # a.one = 1
# # a.two = 55
# # print(a.new_model_instance_fields_dict)
# print(a.__dict__)
# print(a.__class__.__dict__)
# a.save()
