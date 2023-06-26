import cgi
import io
import os
from urllib.parse import parse_qs
from typing import AnyStr, Any

import framework.settings


class Dict(dict):

    def __getitem__(self, item):
        try:
            result = super(Dict, self).__getitem__(item)
        except KeyError:
            return False
        return result[0]


class Request:

    def __init__(self, environ: dict, settings: dict):
        self.environ = environ
        self.settings = settings
        self._build_get_dict(environ['QUERY_STRING'])
        self._build_post_dict(environ['wsgi.input'])
        self.extra = dict()

    def __getattr__(self, item):
        return self.extra.get(item)

    def _build_get_dict(self, param: str) -> None:
        self.GET = Dict(parse_qs(param))

    def _build_post_dict(self, param: io.BytesIO) -> None:
        if 'multipart/form-data' in self.environ.get('CONTENT_TYPE', ''):
            data = cgi.FieldStorage(
                fp=self.environ['wsgi.input'],
                environ=self.environ,
                keep_blank_values=True
            )
            self.POST = dict({'file_to_upload': dict()})
            for val in data.value:
                if not val.filename:
                    v = val.file.read()
                    if v:
                        self.POST.update({val.name: [v]})
                else:
                    file_data = val.file.read()
                    field_path = os.path.join(framework.settings.media, val.filename)
                    self.POST.update({val.name: [field_path]})
                    self.POST['file_to_upload'].update({field_path: file_data})
        else:
            param = param.read().decode('utf-8')
            self.POST = Dict(parse_qs(param))