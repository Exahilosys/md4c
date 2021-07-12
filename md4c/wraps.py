import ctypes

from . import enums
from . import types
from . import details
from . import helpers


__all__ = ()


def _clause(enum, details, func):

    @helpers.enum_cb(enum)
    def wrapper(type, detail_a, udata):
        type = enum(type)
        cls = details.get(type)
        detail = cls.from_address(detail_a) if cls and detail_a else None
        func(type, detail)
        return 0

    return wrapper


_block_details = {
    enums.Block.ul  : details.Ul  ,
    enums.Block.ol  : details.Ol  ,
    enums.Block.li  : details.Li  ,
    enums.Block.h   : details.H   ,
    enums.Block.code: details.Code,
    enums.Block.td  : details.Td
}


def block(func):

    return _clause(enums.Block, _block_details, func)


_span_details = {
    enums.Span.a        : details.A       ,
    enums.Span.img      : details.Img     ,
    enums.Span.wiki_link: details.WikiLink
}


def span(func):

    return _clause(enums.Span, _span_details, func)


def text(func):

    @helpers.enum_cb(enums.Text)
    def wrapper(type, data, size, udata):
        data = data[:size]
        func(type, data)
        return 0

    return wrapper


def debug_log(func):

    def wrapper(message, udata):
        func(message)
        return 0

    return wrapper


def syntax(func):

    def wrapper(*args, **kwargs):
        func()
        return 0

    return wrapper
