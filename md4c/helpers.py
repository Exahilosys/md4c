

__all__ = ()


def c_call(func, *args):

    return func(*(cls(arg) for (cls, arg) in zip(func.argtypes, args)))


def enum_cb(cls, spot = 0):

    def decorator(func):
        def wrapper(*args, **kwargs):
            args = list(args)
            args[spot] = cls(args[spot])
            return func(*args, **kwargs)
        return wrapper

    return decorator
