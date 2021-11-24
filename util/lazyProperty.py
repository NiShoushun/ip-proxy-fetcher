# -*- coding: utf-8 -*-


class LazyProperty(object):
    """
    LazyProperty
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return None
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value
