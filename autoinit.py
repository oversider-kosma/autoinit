#!/bin/env python

from functools import wraps as _wraps
from inspect import isclass as _isclass, isfunction as _isfunction
from warnings import warn as _warn


VERSION = '0.1.0'


class AutoinitWarning(UserWarning, ValueError):
    pass


def autoinit(*decoargs, **decokwargs):
    '''
    Decorator for automatic initialization instance attributes

        @autoinit
        def __init__(self, a, b=10):
            pass

    is equivalent to

        def __init__(self, a, b=10):
            self.a = a
            self.b = b
    Options:
        reverse: bool = False # call real __init__ before setting attributes
        no_warn: bool = False # do not warn when decorator applied to not __init__
    '''
    reverse = decokwargs.get('reverse', False)
    no_warn = decokwargs.get('no_warn', False)

    def inner_decorator(init_or_class):
        if _isclass(init_or_class):
            func = getattr(init_or_class, '__init__')
        elif _isfunction(init_or_class):
            func = init_or_class
        else:
            raise ValueError("autoinit decorator should be applied to class or its __init__ method")

        if (func.__name__  != '__init__' or func.__code__.co_name != '__init__') and not no_warn:
            _warn(AutoinitWarning("autoinit decorator intended to be applied only to __init__ method (use autoinit(no_warn=True) to suppress this warning)"))

        args_names = func.__code__.co_varnames[1:func.__code__.co_argcount]

        @_wraps(func)
        def inner(self, *args, **kwargs):
            if reverse:
                func(self, *args, **kwargs)
            args_vals = args[:] + func.__defaults__[len(args) - len(args_names):]
            for k, v in zip(args_names, args_vals):
                setattr(self, k, v)
            if not reverse:
                func(self, *args, **kwargs)

        if _isclass(init_or_class):
            init_or_class.__init__ = inner
            return init_or_class
        else:
            return inner

    if decoargs and (_isfunction(decoargs[0]) or _isclass(decoargs[0])):
        return inner_decorator(decoargs[0])
    return inner_decorator
