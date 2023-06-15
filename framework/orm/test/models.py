from .base_model import Model, IntField, FloatField, Field, DateField, TextField


class P5(Model):
    temperature = IntField()
    volume = FloatField()


class P6(Model):
    paragraph = Field()
    name = Field()
    summer = FloatField()
    winter = FloatField()


class Tree(Model):
    name = Field()
    koef = FloatField()


class Pich(Model):
    type = Field()
    KKD = FloatField()


class Options(Model):
    recipient = Field()
    v_ch = Field()
    code = IntField()
    address = Field()
    year = IntField()
    zvannya = Field()
    sender = Field()
    contact = Field()


class Request(Model):
    date = DateField()
    p_type = Field()
    result = Field()
    attrs = Field()

    def __str__(self):
        date1 = eval(self.result.replace('\'', '"'))['date1']
        date2 = eval(self.result.replace('\'', '"'))['date2']
        return f'{str(self.date)[:-7]} | {date1} - {date2} | {self.p_type}'


class P4(Model):
    speed = Field()
    type = Field()
    p15 = FloatField()
    p10 = FloatField()
    p5 = FloatField()
    p0 = FloatField()
    m5 = FloatField()
    m10 = FloatField()
    m15 = FloatField()
    m20 = FloatField()
    m25 = FloatField()
    m30 = FloatField()
    m35 = FloatField()
    m40 = FloatField()
    m45 = FloatField()
    m50 = FloatField()


