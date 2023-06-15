import os
import re

from framework.fw.request import Request

FOR_BLOCK_PATTERN = re.compile(
    r'{% for (?P<variable>[a-zA-Z]+) in (?P<seq>[a-zA-Z]+) %}(?P<content>[\S\s]+)(?={% endblock %}){% endblock %}')
VARIABLE_PATTERN = re.compile(r'{{ (?P<variable>[a-zA-Z_]+) }}')


class Engine:

    def __init__(self, base_dir: str, template_dir: str):
        self.template_dir_path = os.path.join(base_dir, template_dir)

    def _get_template_as_string(self, template_name: str) -> str:
        template_path = os.path.join(self.template_dir_path, template_name)
        if not os.path.isfile(template_path):
            raise Exception('template is not file')
        with open(template_path, encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def _build_block(context: dict, raw_template: str) -> str:
        used_var = VARIABLE_PATTERN.findall(raw_template)
        if used_var is None:
            return raw_template
        for var in used_var:
            var_in_template = '{{ %s }}' % var
            raw_template = re.sub(var_in_template, str(context.get(var, '')), raw_template)
        return raw_template

    def _build_block_for(self, context: dict, raw_template: str) -> str:
        for_block = FOR_BLOCK_PATTERN.search(raw_template)
        if for_block is None:
            return raw_template
        build_for = ''
        for i in context.get(for_block.group('seq'), []):
            build_for += self._build_block(
                {for_block.group('variable'): i},
                for_block.group('content')
            )
        template = FOR_BLOCK_PATTERN.sub(build_for, raw_template)
        return template

    def build(self, context: dict, template_name: str) -> str:
        raw_template = self._get_template_as_string(template_name)
        raw_template = self._build_block_for(context, raw_template)
        template = self._build_block(context, raw_template)
        return template


def build_template(request: Request, context: dict, template_name: str) -> str:
    engine = Engine(
        request.settings.get('BASE_DIR'),
        request.settings.get('TEMPLATES_DIR')
    )
    return engine.build(context, template_name)