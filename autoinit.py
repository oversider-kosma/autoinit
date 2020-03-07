#!/bin/env python3

from functools import wraps as _wraps
from inspect import isclass as _isclass, isfunction as _isfunction
from warnings import warn as _warn
from types import MethodType as _MethodType

VERSION = '0.1.0'

class AutoinitWarning(UserWarning, ValueError):
    pass


def autoinit(init_or_class):
    '''Decorator for automatic initialization instance attributes'''
    if _isclass(init_or_class):
        func = getattr(init_or_class, '__init__')
    elif _isfunction(init_or_class):
        func = init_or_class
    else:
        raise ValueError("autoinit decorator should be applied to class or its __init__ method")

    if func.__name__  != '__init__' or func.__code__.co_name != '__init__':
        _warn(AutoinitWarning("autoinit decorator intended to be applied only to __init__ method"))

    args_names = func.__code__.co_varnames[1:func.__code__.co_argcount]

    @_wraps(func)
    def inner(self, *args, **kwargs):
        args_vals = args[:] + func.__defaults__[len(args) - len(args_names):]
        for k, v in zip(args_names, args_vals):
            setattr(self, k, v)
        func(self, *args, **kwargs)

    if _isclass(init_or_class):
        init_or_class.__init__ = inner
        return init_or_class
    else:
        return inner
