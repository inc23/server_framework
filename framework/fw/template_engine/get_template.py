import os
import re

from framework.fw.template_engine.regex import INCLUDE_PATTERN, EXTEND_BLOCK_PATTERN, EXTEND_PATTERN


class GetTemplateAsString:

    def __init__(self, base_dir: list, template_dir: str):
        self.base_dir = base_dir
        self.template_dir = template_dir

    def _get_template_as_string(self, template_name: str) -> str:
        for _dir in self.base_dir:
            template_dir_path = os.path.join(_dir, self.template_dir)
            template_path = os.path.join(template_dir_path, template_name)
            if not os.path.isfile(template_path):
                continue
            with open(template_path, encoding='utf-8') as file:
                return file.read()
        raise Exception('template not is not found')

    def _build_extend(self, raw_template: str) -> str:
        extend_files = EXTEND_PATTERN.finditer(raw_template)
        extending_file = None
        for file in extend_files:
            if file:
                extending_file = self._get_template_as_string(file.group('html_file'))
                break
        if extending_file is None:
            return raw_template
        extend_blocks_in_template = {match.group('block'): match.group('content')
                                     for match in EXTEND_BLOCK_PATTERN.finditer(raw_template)}
        extend_blocks_in_extending_file = {match.group('block'): match.group('content')
                                           for match in EXTEND_BLOCK_PATTERN.finditer(extending_file)}
        extend_blocks_in_extending_file.update(extend_blocks_in_template)
        for block, content in extend_blocks_in_extending_file.items():
            block_pattern = re.compile(rf"{{% block {block} %}}[\S\s]*?{{% endblock %}}")
            extending_file = block_pattern.sub(content, extending_file)
        return extending_file

    def _build_include_block(self, raw_template: str) -> str:
        include_blocks = INCLUDE_PATTERN.finditer(raw_template)
        for block in include_blocks:
            file_name = block.group('html_file')
            file = self._get_template_as_string(file_name)
            raw_template = INCLUDE_PATTERN.sub(file, raw_template, count=1)
        return raw_template

    def get_template(self, template_name):
        template = self._get_template_as_string(template_name)
        template = self._build_extend(template)
        template = self._build_include_block(template)
        return template
