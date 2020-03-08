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
    try:
        autoinit(reverse=False)(7)
    except ValueError:
        pass
    else:
        raise RuntimeError('ValueError wasn\'t raised')

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
