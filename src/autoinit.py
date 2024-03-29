#!/bin/env python
# -*- coding: utf-8 -*-
#pylint: disable=missing-module-docstring

import sys
# from ast import literal_eval
# from os import path
from functools import wraps as _wraps
from inspect import isclass as _isclass,  isfunction as _isfunction
from warnings import warn as _warn


__version__ = "1.1.1"


class AutoinitWarning(UserWarning, ValueError):  # pylint: disable=missing-class-docstring
    pass


def autoinit(*decoargs, **decokwargs):
    '''
    Decorator for automatic initialization instance attributes:
        import autoinit
        class X:
            @autoinit
            def __init__(self, a, b=10):
                pass

    is equivalent to
        class X:
            def __init__(self, a, b=10):
                self.a = a
                self.b = b

    Can be equally applied to both the __init__ method and the entire class.

    Options:
        exclude: str | Iterable[str]
                 skip specified attributes
                 default: []

        no_warn: bool
                 do not warn when decorator applied to not __init__,
                 default: False

        reverse: bool
                 call wrapped method before the assignment
                 default: False
    '''
    reverse = decokwargs.get('reverse', False)
    no_warn = decokwargs.get('no_warn', False)
    exclude = decokwargs.get('exclude', [])

    if sys.version_info.major > 2:
        unicode = str
    else:
        unicode = type(u"")  # pylint: disable=redundant-u-string-prefix
                             # we are running on 2.7 too

    acceptable_str_types = (str, unicode)

    if isinstance(exclude, acceptable_str_types):
        exclude = [exclude]

    def inner_decorator(init_or_class):
        if _isclass(init_or_class):
            func = getattr(init_or_class, '__init__')
        elif _isfunction(init_or_class):
            func = init_or_class
        else:
            raise ValueError("autoinit decorator should be applied to class or its __init__ method")

        if (func.__name__ != '__init__' or func.__code__.co_name != '__init__') and not no_warn:
            _warn(AutoinitWarning("autoinit decorator intended to be applied only to __init__"
                                  " method (use autoinit(no_warn=True) to suppress this warning)"))

        args_names = func.__code__.co_varnames[1:func.__code__.co_argcount]

        @_wraps(func)
        def inner(self, *args, **kwargs):
            if reverse:
                func(self, *args, **kwargs)
            args_vals = args[:]
            if func.__defaults__:
                args_vals += func.__defaults__[len(args) - len(args_names):]

            all_kwargs = dict(zip(args_names, args_vals))
            all_kwargs.update(kwargs)

            for key, val in all_kwargs.items():
                if key not in exclude:
                    if (type(self.__class__).__name__ != 'classobj' and
                            hasattr(self, '__slots__') and key not in self.__slots__):
                        raise AttributeError("Can not assign attribute '%s': it is not "  # pylint:disable=consider-using-f-string
                                             "listed in %s.__slots__" % (key, self.__class__))
                    setattr(self, key, val)
            if not reverse:
                func(self, *args, **kwargs)

        if _isclass(init_or_class):
            init_or_class.__init__ = inner
            return init_or_class
        return inner

    if decoargs and (_isfunction(decoargs[0]) or _isclass(decoargs[0])):
        return inner_decorator(decoargs[0])
    return inner_decorator

_MODULE = sys.modules[__name__]
class _Module (type(_MODULE)): # pylint: disable=too-few-public-methods
    def __init__(self, name, doc = None):
        if sys.version_info.major > 2:
            super().__init__(name, doc)
        else:
            super(_Module, self).__init__(name, doc)  # pylint: disable=bad-super-call, super-with-arguments
        for attr_name in dir(_MODULE):
            setattr(self, attr_name, getattr(_MODULE, attr_name))

    def __call__(self, *decoargs, **decokwargs):
        return autoinit(*decoargs, **decokwargs)

    __doc__ = autoinit.__doc__


sys.modules[__name__] = _Module(__name__)
# so `import autoinit` now works as `from autoinit import autoinit`

del _Module
del _MODULE
