#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""IP core function and group ID definitions
"""

# TODO: load the definitions from an external configuration file

_group_id_name = {
    0: 'undefined',

    11: 'example-group-11',
    22: 'Example group 22'
}
_group_name_id = dict((v, k) for k, v in _group_id_name.items())

assert len(_group_id_name.items()) == len(_group_name_id.items()), \
    "Group ID to name mapping is not unique (duplicate names exist)"

_function_id_name = {
    0: 'undefined',

    45: 'Example function 45',
    76: 'Example function 76'
}
_function_name_id = dict((v, k) for k, v in _function_id_name.items())

assert len(_function_id_name.items()) == len(_function_name_id.items()), \
    "Function ID to name mapping is not unique (duplicate names exist)"


def group_id(key):
    try:
        return _group_name_id[key]
    except:
        return _group_name_id['undefined']

def group_name(key):
    try:
        return _group_id_name[key]
    except:
        return _group_id_name[0]

def function_id(key):
    try:
        return _function_name_id[key]
    except:
        return _function_name_id['undefined']

def function_name(key):
    try:
        return _function_id_name[key]
    except:
        return _function_id_name[0]
