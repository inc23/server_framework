from framework.auth.user import BaseUser
from framework.orm.field import ImageField


class User(BaseUser):

    avatar = ImageField(nullable=True, blank=True, verbose_name='avatar')

    @classmethod
    def order_by(cls):
        return [User.last_name]

    def __str__(self):
        return f'{self.name} {self.last_name}'
