from .base_model import BaseModel
from typing import Type
from .field import BoolField, ImageField


class BaseForm:
    
    model_class: Type[BaseModel] | None = None
    include_field: tuple | str = 'all'

    def __init__(self, obj: BaseModel | None = None):
        self._post_resul_dict = dict()
        self._get_result_dict = dict()
        self._post_dict = None
        self._obj = obj
        self.fields = self.model_class.fields
        if self.include_field == 'all':
            self.include_field = self.model_class.fields.keys()

    def __call__(self, post_dict: dict | None = None):
        if post_dict is None:
            self._build_dict()
        else:
            self._post_dict = post_dict
            self._build_dict()
            self._get_post_dict()
            if not self._obj:
                self._obj = self.model_class()
        return self

    def _get_post_dict(self) -> None:
        for k, v in self._post_dict.items():
            if k != 'file_to_upload':
                self._post_resul_dict.update({k: v[0]})

    def is_valid(self) -> bool:
        is_valid = True
        for k in self.include_field:
            try:
                setattr(self._obj, k, self._post_resul_dict[k])
            except ValueError as e:
                is_valid = False
                self._get_result_dict.update(
                    {f'{k}_label': f'<label for="{k}" style="color: red;"> {e} </label>'})
            except KeyError as e:
                is_valid = False
                self._get_result_dict.update(
                    {f'{k}_label': f'<label for="{k}" style="color: red;"> {k} cant be empty</label>'})
        return is_valid

    def save(self, commit: bool = True) -> None:
        if commit:
            self._obj.save()
            if self._post_dict['file_to_upload']:
                for path, file in self._post_dict['file_to_upload'].items():
                    with open(path, 'wb') as f:
                        f.write(file)

    def _build_dict(self) -> None:
        for k, v in self.fields.items():
            if k in self.include_field:
                placeholder = f'placeholder="input {v.placeholder}"' if v.placeholder else ''
                if self._obj:
                    value = str(getattr(self._obj, k))
                elif self._post_dict:
                    value = self._post_dict.get(k, [''])[0] if not isinstance(v, ImageField) else ''
                else:
                    value = ''
                if isinstance(v, BoolField):
                    checked = 'checked' if value == '1' else ''
                    text = f'<input type="{v.html_type}" {checked} id="{k}" name="{k}" value="1">\n' \
                           f'<input type="hidden" name="{k}" value="0">'
                else:
                    text = f'<input type="{v.html_type}" id="{k}" name="{k}" value="{value}" {placeholder}><br><br>'
                label_text = f'<label for="{k}">{v.verbose_name}</label>'
                self._get_result_dict.update(
                    {
                     f'{k}_label': label_text,
                     k: text
                    }
                )

    @property
    def as_p(self) -> str:
        return '\n'.join(self._get_result_dict.values()) + '<br><br>'

    def __setattr__(self, key, value):
        if key in self.include_field:
            setattr(self._obj, key, value)
        else:
            super(BaseForm, self).__setattr__(key, value)

