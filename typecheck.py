import inspect
import functools


def check_type(terminate=True, debug=False):
    """ 
        terminate: raise a TypeError after found
        debug: extra print func.__name__ and type(func.__name__)    
    """
    def decorate(func):
        def trigger(msg):
            if terminate:
                raise TypeError(msg)
            else:
                print(msg)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            errmsg: str = 'at func "{funcname}", arg "{argname}" expects type "{exptype}", but got type "{errtype}"'
            sig = inspect.signature(func)
            params = sig.parameters
            if debug:
                print(func.__name__)
                print(type(func.__name__))

            # dict args
            for arg_name, arg in kwargs:
                param = params[arg_name]
                if (not isinstance(arg, param.annotation)) and (param.annotation is not inspect._empty):
                    errmsg = errmsg.format(
                        funcname=func.__name__, argname=param.name, exptype=param.annotation, errtype=type(arg))
                    trigger(errmsg)
            # tuple args
            for arg_index, arg in enumerate(args):
                param = list(params.values())[arg_index]
                if (not isinstance(arg, param.annotation)) and (param.annotation is not inspect._empty):
                    errmsg = errmsg.format(
                        funcname=func.__name__, argname=param.name, exptype=param.annotation, errtype=type(arg))
                    trigger(errmsg)
            return func(*args, **kwargs)
        return wrapper
    return decorate




# TEST

@check_type(terminate=False, debug=True)
def func(a: int, b: int, c: int) -> int:
    return a+b+c


def func2() -> float:
    return 0.2

@check_type()
def func3(a: int, b: int, c: int) -> int:
    return a+b+c

func(1, 0.2, func2())
func3(1, 0.2, func2())
