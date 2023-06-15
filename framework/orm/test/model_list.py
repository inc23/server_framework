class ModelList(list):

    def __init__(self, model, get_flag, *args, **kwargs):
        super(ModelList, self).__init__(*args, **kwargs)
        self.model = model
        self.get_flag = get_flag

    def __getattr__(self, item):
        res = []
        for i in self:
            if i[item]:
                res.append(i[item])
        if self.get_flag:
            return res[0]
        return res

    def val_list(self):
        res = []
        for i in self:
            l = list(i.values())
            res.extend(l)
        return res


class StrId(str):

    def __init__(self, model):
        super(StrId, self).__init__()
        self.id = model.id
