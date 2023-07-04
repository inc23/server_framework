# from framework.auth.user import BaseUser
from typing import Type

from app.post.model import Post
from framework.auth.user import BaseUser


class Signal:

    def __init__(self):
        self.signal_dict = dict()

    def send(self, instance):
        sender = instance.model
        if sender in self.signal_dict:
            for func in self.signal_dict[sender]:
                func(instance)

    def connect(self, func, sender):
        if sender in self.signal_dict:
            self.signal_dict[sender].append(func)
        else:
            self.signal_dict[sender] = [func]


save = Signal()
post_update = Signal()
pre_update = Signal()
delete = Signal()


def receiver(signal: Signal, sender):
    def decorator(func):
        signal.connect(func, sender)
        return func
    return decorator


@receiver(signal=pre_update, sender=Post)
def foo(instance):
    print('pre_update')
    print(instance.text)


@receiver(signal=post_update, sender=Post)
def foo(instance):
    print('post_update')
    print(instance.text)


@receiver(signal=delete, sender=Post)
def foo(instance):
    print('delete')
    print(instance.text)