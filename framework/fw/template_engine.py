import os
import re
from .request import Request
from .regex import IF_BLOCK_PATTERN, VARIABLE_PATTERN, FOR_BLOCK_PATTERN, ELIF_BLOCK_PATTERN, ELSE_BLOCK_PATTERN


class IfBlock:

    def __init__(self):
        self._context = None
        self._if_block = None
        self._regular = None
        self._elif_blocks = []
        self._else_block = None
        self._var = None
        self._expression = None
        self._content = None
        self._is_if_block = False
        self._is_else_block = False

    def __call__(
            self,
            context: dict,
            if_block: re,
            is_if_block: bool = True,
            elif_blocks: list | None = None,
            else_block: str | None = None) -> str:
        self._context = context
        self._if_block = if_block
        self._is_if_block = is_if_block
        self._elif_blocks = elif_blocks
        self._else_block = else_block
        self._set_regular()
        self._if_parse_block()
        if self._get_result():
            return self._get_result()
        return self._if_not_result()

    def _if_not_result(self):
        if not self._elif_blocks:
            if not self._else_block:
                return ''
            return self._else_block
        else:
            content = self._elif_blocks.pop(0)
        new_obj = self.__class__()
        return new_obj(
            self._context,
            content,
            False,
            self._elif_blocks,
            self._else_block)

    def _get_result(self) -> str | bool:
        if (self._expression and self._var == self._expression) or self._is_else_block or (
                self._var and not self._expression):
            return self._content
        return False

    def _set_regular(self) -> None:
        if self._is_if_block:
            self._regular = IF_BLOCK_PATTERN
        else:
            self._regular = ELIF_BLOCK_PATTERN

    def _if_parse_block(self) -> None:
        if isinstance(self._if_block, str):
            return None
        self._var = self._resolve_variable(self._if_block.group('variable'))
        self._expression = self._resolve_exp(self._if_block.group('eq'))
        self._content = self._if_block.group('content')
        elif_else_contents = self._if_block.group(
            'else_content') if self._regular == IF_BLOCK_PATTERN else None
        self._elif_else_parse(elif_else_contents)

    def _elif_else_parse(self, elif_else_contents) -> None:
        if elif_else_contents is not None:
            else_blocks = ELSE_BLOCK_PATTERN.finditer(elif_else_contents)
            if else_blocks:
                for else_block in else_blocks:
                    self._else_block = else_block.group('content')
                elif_contents = ELSE_BLOCK_PATTERN.sub('', elif_else_contents)
            else:
                elif_contents = elif_else_contents
            elif_res = ELIF_BLOCK_PATTERN.finditer(elif_contents)
            self._elif_blocks = []
            for elif_re in elif_res:
                self._elif_blocks.append(elif_re)

    def _resolve_variable(self, var: str):
        split_var = var.split('.')
        if len(split_var) == 2:
            var, attr = split_var
            var_from_context = self._context.get(var)
            if hasattr(var_from_context, attr):
                result = getattr(var_from_context, attr)
            else:
                result = None
        else:
            var_from_context = self._context.get(var)
            result = var_from_context
        return result

    def _resolve_exp(self, exp: str):
        if exp:
            split_exp = exp.split('.')
            var_from_context = self._context.get(exp)
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
        self._template_dir_path = os.path.join(base_dir, template_dir)

    def _get_template_as_string(self, template_name: str) -> str:
        template_path = os.path.join(self._template_dir_path, template_name)
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
            raw_template = re.sub(
                var_in_template,
                str(var),
                raw_template,
                count=1)
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
        if if_blocks is None:
            return raw_template
        for if_block in if_blocks:
            if_block_suber = IfBlock()
            if_block_suber = if_block_suber(context, if_block)
            raw_template = IF_BLOCK_PATTERN.sub(
                if_block_suber, raw_template, count=1)
        return raw_template

    def build(self, context: dict, template_name: str) -> str:
        template = self._get_template_as_string(template_name)
        template = self._build_block_for(context, template)
        template = self._build_block_if(context, template)
        template = self._build_block(context, template)
        return template


def build_template(
        request: Request,
        context: dict = None,
        template_name: str = '') -> str:
    engine = Engine(
        request.settings.get('BASE_DIR'),
        request.settings.get('TEMPLATES_DIR')
    )
    if context is None:
        context = dict()
    context.update({'user': request.user})
    return engine.build(context, template_name)
