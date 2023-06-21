import os
import re
from framework.fw.request import Request

FOR_BLOCK_PATTERN = re.compile(
    r'{% for (?P<variable>[a-zA-Z0-9_]+) in (?P<seq>[a-zA-Z0-9_]+) %}(?P<content>[\S\s]+?){% endfor %}'
)
IF_BLOCK_PATTERN = re.compile(
    r'{% if (?P<variable>[a-zA-Z0-9_.]+)( == (?P<eq>[\S\s]+?))? %}(?P<content>[\S\s]+?)((?={% el)(?P<else_content>[\S\s]+?))?{% endif %}'
)

ELIF_BLOCK_PATTERN = re.compile(
    r'{% elif (?P<variable>[a-zA-Z0-9_.]+)( == (?P<eq>[\S\s]*?))? %}(?P<content>[\S\s]*)'
)

ELSE_BLOCK_PATTERN = re.compile(
    r"{% else %}(?P<content>[\S\s]*)"
)

VARIABLE_PATTERN = re.compile(r'{{ (?P<variable>[a-zA-Z0-9_.]+) }}')


class IfBlock:

    def __init__(self):
        self.context = None
        self.if_block = None
        self.regular = None
        self.elif_blocks = []
        self.else_block = None
        self.var = None
        self.expression = None
        self.content = None
        self.is_if_block = False
        self.is_else_block = False

    def __call__(self, context, if_block, is_if_block: bool = True,
                 elif_blocks: list | None = None, else_block: str | None = None):
        self.context = context
        self.if_block = if_block
        self.is_if_block = is_if_block
        self.elif_blocks = elif_blocks
        self.else_block = else_block
        self._set_regular()
        self._if_parse_block()
        if self._get_result():
            return self._get_result()
        return self._if_not_result()

    def _if_not_result(self):
        if not self.elif_blocks:
            if not self.else_block:
                return ''
            return self.else_block
        else:
            content = self.elif_blocks.pop(0)
        new_obj = self.__class__()
        return new_obj(self.context, content, False, self.elif_blocks, self.else_block)

    def _get_result(self):
        if (self.expression and self.var == self.expression) or self.is_else_block or (self.var and not self.expression):
            return self.content
        return False

    def _set_regular(self):
        if self.is_if_block:
            self.regular = IF_BLOCK_PATTERN
        else:
            self.regular = ELIF_BLOCK_PATTERN

    def _if_parse_block(self):
        if isinstance(self.if_block, str):
            return None
        self.var = self._resolve_variable(self.if_block.group('variable'))
        self.expression = self._resolve_exp(self.if_block.group('eq'))
        self.content = self.if_block.group('content')
        elif_else_contents = self.if_block.group('else_content') if self.regular == IF_BLOCK_PATTERN else None
        self._elif_else_parse(elif_else_contents)

    def _elif_else_parse(self, elif_else_contents):
        if elif_else_contents is not None:
            else_blocks = ELSE_BLOCK_PATTERN.finditer(elif_else_contents)
            if else_blocks:
                for else_block in else_blocks:
                    self.else_block = else_block.group('content')
                elif_contents = ELSE_BLOCK_PATTERN.sub('', elif_else_contents)
            else:
                elif_contents = elif_else_contents
            elif_res = ELIF_BLOCK_PATTERN.finditer(elif_contents)
            self.elif_blocks = []
            for elif_re in elif_res:
                self.elif_blocks.append(elif_re)
                    # self.elif_blocks = ['{% elif' + else_content for else_content in elif_else_contents[1:]]

    def _resolve_variable(self, var: str):
        split_var = var.split('.')
        if len(split_var) == 2:
            var, attr = split_var
            var_from_context = self.context.get(var)
            if hasattr(var_from_context, attr):
                result = getattr(var_from_context, attr)
            else:
                result = None
        else:
            var_from_context = self.context.get(var)
            result = var_from_context
        return result

    def _resolve_exp(self, exp: str):
        if exp:
            split_exp = exp.split('.')
            var_from_context = self.context.get(exp)
            if var_from_context is None:
                return exp
            if len(split_exp) == 2:
                var, attr = split_exp
                if hasattr(var_from_context, attr):
                    result = getattr(var_from_context, attr)
                else:
                    result = None
            else:
                result = var_from_context
            return result
        else:
            return exp


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
            raw_template = re.sub(var_in_template, str(var), raw_template, count=1)
        return raw_template

    def _build_block_for(self, context: dict, raw_template: str) -> str:
        for_blocks = FOR_BLOCK_PATTERN.finditer(raw_template)
        if for_blocks is None:
            return raw_template
        for for_block in for_blocks:
            build_for = ''
            for i in context.get(for_block.group('seq'), []):
                context_for_block = {for_block.group('variable'): i}
                context_for_block.update(context)
                content_with_ifs = self._build_block_if(context_for_block, for_block.group('content'))
                build_for += self._build_block(context_for_block, content_with_ifs)
            raw_template = FOR_BLOCK_PATTERN.sub(build_for, raw_template, count=1)
        return raw_template

    @staticmethod
    def _build_block_if(context: dict, raw_template: str) -> str:
        if_blocks = IF_BLOCK_PATTERN.finditer(raw_template)
        if if_blocks is None:
            return raw_template
        for if_block in if_blocks:
            if_block_suber = IfBlock()
            if_block_suber = if_block_suber(context, if_block)
            raw_template = IF_BLOCK_PATTERN.sub(if_block_suber, raw_template, count=1)
        return raw_template

    def build(self, context: dict, template_name: str) -> str:
        template = self._get_template_as_string(template_name)
        template = self._build_block_for(context, template)
        template = self._build_block_if(context, template)
        template = self._build_block(context, template)
        return template


def build_template(request: Request, context: dict = None, template_name: str = '') -> str:
    engine = Engine(
        request.settings.get('BASE_DIR'),
        request.settings.get('TEMPLATES_DIR')
    )
    if context is None:
        context = dict()
    context.update({'user': request.user})
    return engine.build(context, template_name)
