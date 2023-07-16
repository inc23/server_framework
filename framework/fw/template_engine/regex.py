import re


FOR_BLOCK_PATTERN = re.compile(
    r'{% for (?P<variable>\w+) in (?P<seq>[a-zA-Z0-9_.]+) %}(?P<content>[\S\s]+?){% endfor %}'
)


IF_BLOCK_PATTERN = re.compile(
    r'{% if (?P<variable>[a-zA-Z0-9_.]+)( == (?P<eq>[\S\s]+?))? %}(?P<content>[\S\s]+?)((?={% el)'
    r'(?P<else_content>[\S\s]+?))?{% endif %}')

ELIF_BLOCK_PATTERN = re.compile(
    r'{% elif (?P<variable>[a-zA-Z0-9_.]+)( == (?P<eq>[\S\s]*?))? %}(?P<content>[\S\s]*?)(?={% e|$)'

)

ELSE_BLOCK_PATTERN = re.compile(
    r"{% else %}(?P<content>[\S\s]*)"
)

VARIABLE_PATTERN = re.compile(r'{{ (?P<variable>[a-zA-Z0-9_.]+) }}')


URL_PATTERN = re.compile(r'{% url (?P<namespace>\w+):(?P<name>\w+) (?P<arg>\w+) %}')


INCLUDE_PATTERN = re.compile(r"{% include '(?P<html_file>[a-zA-Z0-9_.]+)' %}")


EXTEND_PATTERN = re.compile(r"{% extend '(?P<html_file>[a-zA-Z0-9_.]+)' %}")


EXTEND_BLOCK_PATTERN = re.compile(
    r'{% block (?P<block>\w+) %}(?P<content>[\S\s]+?)?{% endblock %}'
)

STATIC_PATTERN = re.compile(r"{% static '(?P<file>[\S\s]+?)' %}")