from urllib.parse import parse_qs

from .base_model import BaseModel, MetaModel
from typing import Type, Tuple
from .field import BoolField, ImageField
from ..fw.request import Request


class BaseForm:
    
    model_class: Type[BaseModel] | None = None
    include_field: tuple | str = 'all'

    def __init__(self, request: Request, obj: BaseModel | None = None):
        self._request = request
        self._post_resul_dict = dict()
        self._get_result_dict = dict()
        self._post_dict = None
        self.csrf = self._get_csrf_token()
        self._obj = obj
        self.fields = self.model_class.fields
        if self.include_field == 'all':
            self.include_field = self.model_class.fields.keys()

    def __call__(self, post_dict: dict | None = None):
        if post_dict is None:
            self._build_dict_with_html()
        else:
            self._post_dict = post_dict
            self._build_dict_with_html()
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
        if self._post_dict['csrf_token'][0] != self._request.csrf_token:
            is_valid = False
        for k in self.include_field:
            try:
                setattr(self._obj, k, self._post_resul_dict[k])
            except ValueError as e:
                is_valid = False
                self._get_result_dict.update(
                    {f'{k}_label': f'<label for="{k}" style="color: red;"> {e} </label>'})
            except KeyError:
                if not self.fields.get(k).blank:
                    is_valid = False
                    self._get_result_dict.update(
                            {f'{k}_label': f'<label for="{k}" style="color: red;"> {k} cant be empty</label>'})
            if self.model_class.fields[k].unique \
                    and self.model_class.objects.get(getattr(self.model_class, k) == self._post_resul_dict.get(k)):
                self._get_result_dict.update(
                    {f'{k}_label': f'<label for="{k}" style="color: red;"> {k} have to be unique</label>'})
                is_valid = False
        return is_valid

    def save(self, commit: bool = True) -> None:
        if commit:
            self._obj.save()
            if self._post_dict['file_to_upload']:
                for path, file in self._post_dict['file_to_upload'].items():
                    with open(path, 'wb') as f:
                        f.write(file)

    def _build_dict_with_html(self) -> None:
        for k, v in self.fields.items():
            if k in self.include_field:
                if self._obj:
                    value = str(getattr(self._obj, k))
                elif self._post_dict:
                    value = self._post_dict.get(k, [''])[0] if not isinstance(v, ImageField) else ''
                else:
                    value = ''
                text, label_text = self._build_html_for_field(k, v, value)
                self._get_result_dict.update(
                    {
                     f'{k}_label': label_text,
                     k: text
                    }
                )

    @staticmethod
    def _build_html_for_field(name, field, value) -> Tuple[str, str]:
        placeholder = f'placeholder="input {field.placeholder}"' if field.placeholder else ''
        label_text = f'<label for="{name}">{field.verbose_name}</label>'
        if isinstance(field, BoolField):
            checked = 'checked' if value == '1' else ''
            text = f'<input type="{field.html_type}" {checked} id="{name}" name="{name}" value="1">\n' \
                   f'<input type="hidden" name="{name}" value="0">'
        elif field.foreign_key and not field.choices:
            foreign_model_name, foreign_field = field.foreign_key.split('.')
            foreign_model: BaseModel = MetaModel.classes_dict[foreign_model_name]
            text = f'<select name="{name}"id="{name}">\n'
            for obj in foreign_model.objects.all():
                text += f'<option value="{getattr(obj, foreign_field)}"> {obj} </option>\n'
            text += '</select>'
        elif field.choices:
            text = f'<select name="{name}"id="{name}">\n'
            for val, val_name in field.choices:
                text += f'<option value="{val}"> {val_name} </option>\n'
            text += '</select>'
        else:
            text = f'<input type="{field.html_type}" id="{name}" name="{name}" value="{value}" {placeholder}><br><br>'
        return text, label_text

    @property
    def as_p(self) -> str:
        return '\n'.join(self._get_result_dict.values()) + '<br><br>'

    def _get_csrf_token(self):
        csrf = self._request.csrf_token
        return f'<input type ="hidden" name="csrf_token" value={csrf}>'

    def __getattr__(self, item):
        return self._get_result_dict.get(item)

    def __setattr__(self, key, value):
        if key in self.include_field:
            setattr(self._obj, key, value)
        else:
            super(BaseForm, self).__setattr__(key, value)
