import os
import re

FOR_BLOCK_PATTERN = re.compile(
    r'{% for (?P<variable>[a-zA-Z]+) in (?P<seq>[a-zA-Z]+) %}(?P<content>[\S\s]+)(?={% endblock %}){% endblock %}')
VARIABLE_PATTERN = re.compile(r'{{ (?P<variable>[a-zA-Z_]+) }}')


