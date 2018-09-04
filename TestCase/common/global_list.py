#!/usr/bin/python
# -*- coding: utf-8 -*-


def _init():
    global _global_data
    _global_data = {}

def set_value(name, value):
    _global_data[name] = value


def get_value(name, defValue=None):
    try:
        return _global_data[name]

    except KeyError:
        return defValue