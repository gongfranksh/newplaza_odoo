# -*- coding: utf-8 -*-
def bnfunlog(*args, **kwargs):
    def _bnfunlog(func):
        def __bnfunlog(*args, **kwargs):
            func(*args, **kwargs)
            print("Process %s  is called" % (func.__name__))
        return __bnfunlog
    return _bnfunlog

def funclog(func):
    def wrapper(*args, **kwargs):
        # print(sys._getframe().f_code.co_name)
        print(args)
        func(*args, **kwargs)
    return  wrapper

def deco(arg):
    def _deco(func):
        def __deco(*args, **kwargs):
            print("before %s called [%s]." % (func.__name__, arg))
            func(*args, **kwargs)
            print("  after %s called [%s]." % (func.__name__, arg))
        return __deco
    return _deco


def singleton(cls):
    instances = {}

    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton