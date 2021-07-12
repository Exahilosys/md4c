import ctypes
import functools

from . import types
from . import enums


__all__ = ('Attribute', 'Ul', 'Ol', 'Li', 'H', 'Code', 'Td', 'A', 'Img',
           'WikiLink')


_Base = ctypes.Structure


class _Meta(_Base.__class__):

    _types = {
        ctypes.c_bool      : bool,
        ctypes.c_char      : str,
        ctypes.c_wchar     : str,
        ctypes.c_byte      : bytes,
        ctypes.c_ubyte     : bytes,
        ctypes.c_short     : int,
        ctypes.c_ushort    : int,
        ctypes.c_int       : int,
        ctypes.c_uint      : int,
        ctypes.c_long      : int,
        ctypes.c_ulong     : int,
        ctypes.c_longlong  : int,
        ctypes.c_ulonglong : int,
        ctypes.c_size_t    : int,
        ctypes.c_ssize_t   : int,
        ctypes.c_float     : float,
        ctypes.c_double    : float,
        ctypes.c_longdouble: float,
        ctypes.c_char_p    : bytes,
        ctypes.c_wchar_p   : str,
        ctypes.c_void_p    : int
    }

    @property
    def __doc__(self):

        try:
            subdoc = self.__dict__['__doc__']
            (value, descriptions) = subdoc.rsplit('\n\n', 1)
            descriptions = descriptions.split('\n')
            (names, c_types) = zip(*self._fields_)
            rows = []
            def draw(value):
                buffer = ':class:`'
                if issubclass(value, _Base):
                    buffer += '.'
                else:
                    value = self._types[value]
                return f'{buffer}{value.__name__}`\\'
            for (name, c_type, descr) in zip(names, c_types, descriptions):
                type = draw(c_type)
                descr = descr.strip()
                row = f'    "{name}", {type}, "{descr}"'
                rows.append(row)
            if rows:
                rows = '\n'.join(rows)
                outline = (
f"""
.. csv-table::
    :header: Name, Type, Description
    :widths: auto

{rows}
"""
)
                value = f'{value}\n\n{outline}'
        except Exception as error:
            print(repr(error))

        return value


class Detail(_Base, metaclass = _Meta):

    _fields_ = ()


class Attribute(Detail):

    """
    Wraps strings that are outside of a normal text flow and are propagated
    within various detailed structures, but still may contain string portions
    of different types like e.g. entities.

    n/a
    n/a
    n/a
    n/a
    """

    _fields_ = (
        ('text'          , types.char_p),
        ('size'          , types.size  ),
        ('substr_types'  , types.enum  ),
        ('substr_offsets', types.offset)
    )


class Ul(Detail):

    """
    ..

    Non-zero if tight list, zero if loose.
    Item bullet character of the list, e.g. ``-``, ``+``, ``+``.
    """

    _fields_ = (
        ('is_tight'   , ctypes.c_int),
        ('mark'       , types.char  )
    )


class Ol(Detail):

    """
    ..

    First index of the ordered list.
    Non-zero if tight list, zero if loose.
    Character delimiting the item marks in md source, e.g. ``.`` or ``)``
    """

    _fields_ = (
        ('start'         , ctypes.c_uint),
        ('is_tight'      , ctypes.c_int ),
        ('mark_delimiter', types.char   )
    )


class Li(Detail):

    """
    ..

    Can be non-zero only with :class:`~.flags.Spec`'s ``task_lists``.
    If ``is_task``, it's ``x``, ``X`` or single space. ``None`` otherwise.
    If ``is_task``, offset in the input of the char between ``(`` and ``)``.
    """

    _fields_ = (
        ('is_task'         , ctypes.c_int),
        ('task_mark'       , types.char  ),
        ('task_mark_offset', types.offset)
    )


class H(Detail):

    """
    ..

    Header level (1 to 6)
    """

    _fields_ = (
        ('level', ctypes.c_uint),
    )


class Code(Detail):

    """
    ..

    n/a
    The language's syntax name.
    The character used for fenced code block; or zero for indented code block.
    """

    _fields_ = (
        ('info'      , Attribute ),
        ('lang'      , Attribute ),
        ('fence_char', types.char)
    )


class Td(Detail):

    """
    ..

    n/a
    """

    _fields_ = (
        ('align', types.enum),
    )


class A(Detail):

    """
    ..

    n/a
    n/a
    """

    _fields_ = (
        ('href' , Attribute),
        ('title', Attribute)
    )


class Img(Detail):

    """
    ..

    n/a
    n/a
    """

    _fields_ = (
        ('src'  , Attribute),
        ('title', Attribute)
    )


class WikiLink(Detail):

    """
    ..

    n/a
    """

    _fields_ = (
        ('target', Attribute),
    )
