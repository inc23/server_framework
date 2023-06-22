from .base_model import BaseModel


class BaseForm:
    
    model_class: BaseModel | None = None
    include_field: tuple | str = 'all'

    def __init__(self):
        self.result_dict = {}
        if self.include_field == 'all':
            self.include_field = self.model_class.fields.keys()
        for k, v in self.model_class.fields.items():
            if k in self.include_field:
                text = f'<input name="{k}">'
                self.result_dict.update({k: text, f'{k}_label': v.verbose_name})

    def __getattr__(self, item):
        return self.result_dict[item]



