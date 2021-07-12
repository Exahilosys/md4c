import ctypes

from . import types
from . import protos
from . import wraps


__all__ = ()


class Storage(ctypes.Structure):

    _fields_ = (
        ('api_version', ctypes.c_uint   ),
        ('flags',       ctypes.c_uint   ),
        ('enter_block', protos.clause   ),
        ('leave_block', protos.clause   ),
        ('enter_span',  protos.clause   ),
        ('leave_span',  protos.clause   ),
        ('text',        protos.text     ),
        ('debug_log',   protos.debug_log),
        ('syntax',      protos.syntax)
    )


_nerrcheck = lambda *a: 0


_functions = (
    (
        'md_parse',
        (
            types.char_p,
            types.size,
            ctypes.POINTER(Storage),
            types.void
        ),
        types.ires,
        _nerrcheck
    ),
)


def load(path):

    """
    Load the library and fix all exposed functions.
    """

    lib = ctypes.CDLL(path)

    for (name, argtypes, restype, errcheck) in _functions:
        func = getattr(lib, name)
        func.argtypes = argtypes
        func.restype = restype
        func.errcheck = errcheck

    return lib


_noop = lambda *a, **k: 0


_assets = (
    (None           , 0    ),
    (None           , 0    ),
    (wraps.block    , _noop),
    (wraps.block    , _noop),
    (wraps.span     , _noop),
    (wraps.span     , _noop),
    (wraps.text     , _noop),
    (wraps.debug_log, _noop),
    (None           , _noop),
)


def create(**options):

    """
    Get the struct holding all callbacks.
    """

    args = []

    (names, funcs) = zip(*Storage._fields_)

    (wraps, fails) = zip(*_assets)

    for (name, fail, func, wrap) in zip(names, fails, funcs, wraps):
        value = options.get(name) or fail
        if wrap:
            value = wrap(value)
        value = func(value)
        args.append(value)

    return Storage(*args)
