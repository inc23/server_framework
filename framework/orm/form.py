from .base_model import BaseModel
from typing import Type


class BaseForm:
    
    model_class: Type[BaseModel] | None = None
    include_field: tuple | str = 'all'

    def __init__(self, post_dict: dict | None = None):
        self.get_result_dict = dict()
        if post_dict is None:
            self._build_dict()
        else:
            self.post_resul_dict = dict()
            self.post_dict = post_dict
            self._get_post_dict()
            self.obj = self.model_class()

    def _get_post_dict(self) -> None:
        for k, v in self.post_dict.items():
            self.post_resul_dict.update({k: v[0]})

    def is_valid(self) -> bool:
        print(self.post_resul_dict)
        print(self.obj.fields)
        for k, v in self.post_resul_dict.items():
            try:
                print(f'{k} = {v}')
                setattr(self.obj, k, v)
            except ValueError as e:
                print(e)
                return False
        return True

    def save(self, commit: bool = True) -> None:
        if commit:
            self.obj.save()

    def _build_dict(self) -> None:
        if self.include_field == 'all':
            self.include_field = self.model_class.fields.keys()
        for k, v in self.model_class.fields.items():
            if k in self.include_field:
                text = f'<input name="{k}">'
                self.get_result_dict.update({k: text, f'{k}_label': v.verbose_name})

    # def __getattr__(self, item):
    #     return self.result_dict[item]

    @property
    def as_p(self) -> str:
        return '<br><br>\r\n'.join(self.get_result_dict.values()) + '<br>'

    def __setattr__(self, key, value):
        if key in self.include_field:
            setattr(self.obj, key, value)
        else:
            super(BaseForm, self).__setattr__(key, value)

