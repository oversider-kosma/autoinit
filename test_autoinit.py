#!/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=no-member, unused-variable

import pytest
from sys import version_info

from autoinit import autoinit, AutoinitWarning


class Base_obj(object): pass
class Base: pass


def class_with_deco_builder(from_object=False):
    @autoinit
    class C(Base_obj if from_object else Base):
        def __init__(self, a, b='default value'):
            self.c = 'in init value'
    return C


def class_with_decorated_method_builder(from_object=True):
    class C(Base_obj if from_object else Base):
        @autoinit
        def __init__(self, a, b='default value'):
            self.c = 'in init value'
    return C


def test_classdecorator():
    C = class_with_deco_builder()
    inst = C(1)
    assert inst.a == 1
    assert inst.b == 'default value'
    assert inst.c == 'in init value'


if version_info.major == 2:
    def test_classdecorator_newstyle():
        C = class_with_deco_builder(from_object=True)
        inst = C(1)
        assert inst.a == 1
        assert inst.b == 'default value'
        assert inst.c == 'in init value'


def test_methoddecorator():
    C = class_with_decorated_method_builder()
    inst = C(1)
    assert inst.a == 1
    assert inst.b == 'default value'
    assert inst.c == 'in init value'


if version_info.major == 2:
    def test_methoddecorator_newstyle():
        C = class_with_decorated_method_builder(from_object=True)
        inst = C(1)
        assert inst.a == 1
        assert inst.b == 'default value'
        assert inst.c == 'in init value'


def test_warning_is_thrown():
    with pytest.warns(AutoinitWarning):
        class C(Base):
            @autoinit
            def not_init(self, a, b='default value'):
                self.c = 'in init value'


def test_warning_suppression():
    try:
        class C(Base):
            @autoinit(no_warn=True)
            def not_init(self, a, b='default value'):
                self.c = 'in init value'
    except AutoinitWarning:
        raise RuntimeError('AutoinitWarning was warned but should be suppressed')


def test_exception():
    with pytest.raises(ValueError):
        autoinit(reverse=False)(7)


def test_noreverse():
    class C(Base_obj):
        @autoinit
        def __init__(self, a, b=2):
            assert self.b == 2
    assert C(1).a == 1


def test_reverse():
    class C(Base_obj):
        @autoinit(reverse=True)
        def __init__(self, a, b=2):
            assert not hasattr(self, 'a')
            assert not hasattr(self, 'b')
    inst = C(1)
    assert inst.a == 1
    assert inst.b == 2


def test_init_noargs():
    @autoinit
    class C(Base_obj):
        def __init__(self):
           self.q = 5
    assert C().q == 5


if version_info.major == 2:
    def test_init_noargs_oldstyle():
        @autoinit
        class C:
            def __init__(self):
                self.q = 5
        assert C().q == 5


def test_exclude_one():
    class C(Base_obj):
        @autoinit(exclude='b')
        def __init__(self, a, b, c):
            pass
    inst = C(1, 2, 3)
    assert not hasattr(inst, 'b')


def test_exclude_many():
    @autoinit(exclude=['b', 'c'])
    class C(Base_obj):
        def __init__(self, a, b, c):
            assert not hasattr(self, 'b')

    inst = C(1, 2, 3)
    assert not hasattr(inst, 'c')

def test_slots():
    @autoinit
    class C(Base_obj):
        __slots__ = ['a', 'b']
        def __init__(self, a, b):
            pass
    inst = C(1, 2)
    assert inst.a == 1 and inst.b == 2

def test_slots_raises():
    with pytest.raises(AttributeError):
        @autoinit
        class C(Base_obj):
            __slots__ = ['a', 'b']
            def __init__(self, a, b, c=3):
                pass
        inst = C(1, 2)

def test_slots_excluded_not_raises():
    @autoinit(exclude='c')
    class C(Base_obj):
        __slots__ = ['a', 'b']
        def __init__(self, a, b, c=3):
            pass
    inst = C(1, 2)
    assert not hasattr(inst, 'c')

if version_info.major == 2:
    def test_oldstyle_class_not_raises():
        @autoinit
        class C:
            __slots__ = ['a', 'b']
            def __init__(self, a, b, c=3):
                pass
        inst = C(1, 2)
        assert inst.c == 3
