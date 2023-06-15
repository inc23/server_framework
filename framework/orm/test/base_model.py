from datetime import datetime

from .manager import Manager


class Field:

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, type=None) -> object:
        return obj.field_dict.get(self.name) or None

    def __set__(self, obj, value) -> None:
        obj.field_dict[self.name] = str(value)


class TextField(Field):

    def __get__(self, obj, type=None) -> object:
        return str(obj.field_dict.get(self.name))


class FloatField(Field):

    def __set__(self, obj, value) -> None:
        if value is None:
            obj.field_dict[self.name] = value
        else:
            try:
                value = float(value)
            except ValueError:
                pass
            except TypeError:
                pass
            else:
                obj.field_dict[self.name] = float(value)


class IntField(Field):

    def __set__(self, obj, value) -> None:
        if value is None:
            obj.field_dict[self.name] = value
        else:
            try:
                value = int(value)
            except ValueError:
                pass
            except TypeError:
                pass
            else:
                obj.field_dict[self.name] = int(value)


class DateField(Field):
    def __get__(self, obj, type=None) -> object:
        if isinstance(obj.field_dict.get(self.name), float):
            return datetime.fromtimestamp(obj.field_dict.get(self.name))
        return obj.field_dict.get(self.name) or None

    def __set__(self, obj, value) -> None:
        if isinstance(value, datetime):
            obj.field_dict[self.name] = value.timestamp()
        else:
            obj.field_dict[self.name] = value


class MetaModel(type):

    def __new__(mcs, class_name, parents, attrs):
        fields = {'id': None}
        for k, v in attrs.items():
            if isinstance(v, Field):
                fields[k] = v
        model = super(MetaModel, mcs).__new__(mcs, class_name, parents, attrs)
        setattr(model, 'model_name', attrs['__qualname__'].lower())
        setattr(model, 'fields', fields)
        setattr(model, 'objects', Manager(model))
        return model


class Model(metaclass=MetaModel):

    def __init__(self, *args, **kwargs):
        super(Model, self).__init__()
        self.field_dict = dict()
        if kwargs:
            for k in self.fields.keys():
                setattr(self, k, kwargs.get(k, None))

    def save(self):
        self.objects.save(self.field_dict)