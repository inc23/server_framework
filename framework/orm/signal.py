from settings import apps, app_name


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


for app in apps:
    try:
        __import__(f'{app_name}.{app}.signal')
    except ModuleNotFoundError:
        continue
