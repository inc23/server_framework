import os
import re
from settings import web_socket, static_html
from framework.fw.request import Request
from .block_if import IfBlock
from .get_template import GetTemplateAsString
from .regex import IF_BLOCK_PATTERN, VARIABLE_PATTERN, FOR_BLOCK_PATTERN, URL_PATTERN, STATIC_PATTERN


class Engine:

    def __init__(self, raw_template: str, url_list: list):
        self.url_list = url_list
        self.raw_template = raw_template

    @staticmethod
    def _resolve_variable(context: dict, var: str) -> str:
        split_var = var.split('.')
        if len(split_var) == 2:
            var, attr = split_var
            var = getattr(context.get(var, ''), attr)
        else:
            var = context.get(var, '')
        return var

    def _build_block(self, context: dict, raw_template: str) -> str:
        used_var = VARIABLE_PATTERN.findall(raw_template)
        if used_var is None:
            return raw_template
        for var in used_var:
            var_in_template = '{{ %s }}' % var
            var = self._resolve_variable(context, var)
            raw_template = re.sub(
                var_in_template,
                str(var),
                raw_template,
                count=1)
        return raw_template

    def _build_block_for(self, context: dict, raw_template: str) -> str:
        for_blocks = FOR_BLOCK_PATTERN.finditer(raw_template)
        for for_block in for_blocks:
            build_for = ''
            for i in context.get(for_block.group('seq'), []):
                context_for_block = {for_block.group('variable'): i}
                context_for_block.update(context)
                content_with_ifs = self._build_block_if(
                    context_for_block, for_block.group('content'))
                build_for += self._build_block(context_for_block,
                                               content_with_ifs)
            raw_template = FOR_BLOCK_PATTERN.sub(
                build_for, raw_template, count=1)
        return raw_template

    @staticmethod
    def _build_block_if(context: dict, raw_template: str) -> str:
        if_blocks = IF_BLOCK_PATTERN.finditer(raw_template)
        for if_block in if_blocks:
            if_block_suber = IfBlock()
            if_block_suber = if_block_suber(context, if_block)
            raw_template = IF_BLOCK_PATTERN.sub(
                if_block_suber, raw_template, count=1)
        return raw_template

    def _url_block(self, raw_template: str) -> str:
        used_urls = URL_PATTERN.finditer(raw_template)
        for url_re in used_urls:
            name = url_re.group('name')
            namespace = url_re.group('namespace')
            arg = url_re.group('arg') if url_re.group('arg') else ''
            for path in self.url_list:
                if path.namespace == namespace:
                    for p in path.include:
                        if p.name == name:
                            url = f'{web_socket}{path.url}{p.url}{arg}'
                            raw_template = URL_PATTERN.sub(url, raw_template, count=1)
        return raw_template

    @staticmethod
    def _build_static(raw_template):
        static_files = STATIC_PATTERN.finditer(raw_template)
        for file_in_template in static_files:
            file = file_in_template.group('file')
            path_file = os.path.join(static_html, file)
            raw_template = STATIC_PATTERN.sub(path_file, raw_template, count=1)
        return raw_template

    def build(self, context: dict, template: str) -> str:
        template = self._build_block_for(context, template)
        template = self._build_block_if(context, template)
        template = self._build_block(context, template)
        template = self._url_block(template)
        template = self._build_static(template)
        return template


def build_template(
        request: Request,
        context: dict = None,
        template_name: str = '') -> str:

    raw_template = GetTemplateAsString(
        request.settings.get('BASE_DIR'),
        request.settings.get('TEMPLATES_DIR')
    ).get_template(template_name)

    engine = Engine(
        url_list=request.url_list,
        raw_template=raw_template
    )
    return engine.build(context, raw_template)
