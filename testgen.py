# -*- coding: utf-8 -*-

"""Generate Syntax-Valid Test Instances with Full Coverage for SysY

CAUTION: Require 10GB+ System Memory & 5GB+ System Storage Space
Grammer: grammer.yaml
Test Instances: instances.c
"""

from typing import List
import yaml
import re
import itertools

__author__ = "Daniel (danielw10001@gmail.com)"
__docformat__ = 'reStructuredText'

with open('grammer.yaml') as file:
    GRAMMER: Dict[str, List[str]] = yaml.safe_load(file)
    """:var GRAMMER: {GRAMMER_UNIT: ['SPAN']}"""
INSTANCE: Dict[str, List[str]] = {unit: [] for unit in GRAMMER.keys()}
"""var INSTANCE: {GRAMMER_UNIT: ['INSTANCE']}"""


def get_instances(unit: str) -> List[str]:
    """Get Unit Instances"""
    global GRAMMER
    global INSTANCE

    while len(GRAMMER[unit]) > 0:
        # Still have span to generate
        span = GRAMMER[unit].pop(0)
        span_instances = []
        for token in re.split(r'([A-Z][a-zA-Z]*)', span):  # Tokenlize
            if not re.fullmatch(r'[A-Z][a-zA-Z]*', token):
                # Terminate string
                if not span_instances:
                    # No instances yet
                    span_instances.append(token)
                else:
                    span_instances = [inst+token
                                      for inst in span_instances]
            else:
                # Non-Terminate String
                if not span_instances:
                    # No instances yet
                    span_instances.extend(get_instances(token))
                else:
                    tokenstrs = get_instances(token)

                    # Align
                    if len(span_instances) > len(tokenstrs):
                        tokenstrs = itertools.cycle(tokenstrs)
                    else:
                        span_instances = itertools.cycle(span_instances)

                    span_instances = [inst+tokenstr for inst, tokenstr in
                                      zip(span_instances, tokenstrs)]
        INSTANCE[unit].extend(span_instances)
    return INSTANCE[unit]


with open('instances.c', 'w') as outfile:
    print(*get_instances('CompUnit'), sep="\n", file=outfile)
