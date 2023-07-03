from framework.auth.user import BaseUser


class User(BaseUser):

    @classmethod
    def order_by(cls):
        return [User.last_name]

    def __str__(self):
        return f'{self.name} {self.last_name}'