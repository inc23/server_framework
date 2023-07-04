import re


FOR_BLOCK_PATTERN = re.compile(
    r'{% for (?P<variable>\w+) in (?P<seq>\w+) %}(?P<content>[\S\s]+?){% endfor %}'
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