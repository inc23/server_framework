from framework.orm.signal import receiver, pre_update, post_update, delete
from app.post.model import Post


@receiver(signal=pre_update, sender=Post)
def foo1(instance):
    print('pre_update')
    print(instance.text)


@receiver(signal=post_update, sender=Post)
def foo2(instance):
    print('post_update')
    print(instance.text)


@receiver(signal=delete, sender=Post)
def foo3(instance):
    print('delete')
    print(instance.text)