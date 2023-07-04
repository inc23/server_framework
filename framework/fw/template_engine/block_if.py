import re
from framework.fw.template_engine.regex import IF_BLOCK_PATTERN, ELIF_BLOCK_PATTERN, ELSE_BLOCK_PATTERN


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
