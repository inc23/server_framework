from .base_model import BaseModel
from typing import Type


class BaseForm:
    
    model_class: Type[BaseModel] | None = None
    include_field: tuple | str = 'all'

    def __init__(self, obj: BaseModel | None = None):
        self.post_resul_dict = dict()
        self.get_result_dict = dict()
        self.obj = obj
        if self.include_field == 'all':
            self.include_field = self.model_class.fields.keys()

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
        is_valid = True
        for k in self.include_field:
            try:
                setattr(self.obj, k, self.post_resul_dict[k])
            except ValueError as e:
                is_valid = False
                self.get_result_dict.update(
                    {f'{k}_label': f'<label for="{k}" style="color: red;"> wrong {k} value </label>'})
                print(e)
            except KeyError as e:
                is_valid = False
                self.get_result_dict.update(
                    {f'{k}_label': f'<label for="{k}" style="color: red;"> field {k} must be filled</label>'})
                print(e)
        return is_valid

    def save(self, commit: bool = True) -> None:
        if commit:
            self.obj.save()

    def _build_dict(self) -> None:
        for k, v in self.model_class.fields.items():
            if k in self.include_field:
                placeholder = f'placeholder="input {v.placeholder}"' if v.placeholder else ''
                value = str(getattr(self.obj, k)) if self.obj else ''
                text = f'<input type="{v.html_type}" id="{k}" name="{k}" value="{value}" {placeholder}><br><br>'
                self.get_result_dict.update(
                    {
                     f'{k}_label': f'<label for="{k}">{v.verbose_name}</label>',
                     k: text
                    }
                )

    @property
    def as_p(self) -> str:
        return ''.join(self.get_result_dict.values()) + '<br>'

    def __setattr__(self, key, value):
        if key in self.include_field:
            setattr(self.obj, key, value)
        else:
            super(BaseForm, self).__setattr__(key, value)

