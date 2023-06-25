from .base_model import BaseModel
from typing import Type


class BaseForm:
    
    model_class: Type[BaseModel] | None = None
    include_field: tuple | str = 'all'

    def __init__(self, obj: BaseModel | None = None):
        self.post_resul_dict = dict()
        self.get_result_dict = dict()
        self.obj = obj

    def __call__(self, post_dict: dict | None = None):
        if post_dict is None:
            self._build_dict()
        else:
            self.post_dict = post_dict
            self._get_post_dict()
            if not self.obj:
                self.obj = self.model_class()
        return self

    def _get_post_dict(self) -> None:
        for k, v in self.post_dict.items():
            self.post_resul_dict.update({k: v[0]})

    def is_valid(self) -> bool:
        print(self.post_resul_dict)
        for k, v in self.post_resul_dict.items():
            try:
                print(f'{k} = {v}')
                setattr(self.obj, k, v)
            except ValueError as e:
                self.get_result_dict.update({f'{k}_label': f'<label for="{k}"> style="color: red;"> wrong value {k}</label>'})
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
                placeholder = f'placeholder="input {v.placeholder}"' if v.placeholder else ''
                if self.obj:
                    text = f'<input type="text" id="{k}" name="{k}" value="{getattr(self.obj, k)}" {placeholder}><br><br>'
                else:
                    text = f'<input type="text" id="{k}"  name="{k}" {placeholder}><br><br>'
                self.get_result_dict.update(
                    {
                     f'{k}_label': f'<label for="{k}">{v.verbose_name}</label>',
                        k: text
                    }
                )
        print(self.get_result_dict)

    @property
    def as_p(self) -> str:
        return ''.join(self.get_result_dict.values()) + '<br>'

    def __setattr__(self, key, value):
        if key in self.include_field:
            setattr(self.obj, key, value)
        else:
            super(BaseForm, self).__setattr__(key, value)

