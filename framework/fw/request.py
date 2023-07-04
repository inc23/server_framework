import cgi
import io
import os
from urllib.parse import parse_qs
from framework import settings


class PostDict(dict):

    def __getitem__(self, item):
        try:
            result = super(PostDict, self).__getitem__(item)
        except KeyError:
            return False
        return result[0]


class Request:

    def __init__(self, environ: dict, setting: dict, url_list: list):
        self.environ = environ
        self.settings = setting
        self.url_list = url_list
        self._build_get_dict(environ['QUERY_STRING'])
        self._build_post_dict(environ['wsgi.input'])
        self.extra = dict()

    def __getattr__(self, item):
        return self.extra.get(item)

    def _build_get_dict(self, param: str) -> None:
        self.GET = PostDict(parse_qs(param))

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
                    if v and val.name not in self.POST:
                        self.POST.update({val.name: [v]})
                else:
                    file_data = val.file.read()
                    field_path_for_db = os.path.join(settings.media_folder, val.filename)
                    field_path = os.path.join(settings.media, val.filename)
                    self.POST.update({val.name: [field_path_for_db]})
                    self.POST['file_to_upload'].update({field_path: file_data})
        else:
            param = param.read().decode('utf-8')
            self.POST = (parse_qs(param))