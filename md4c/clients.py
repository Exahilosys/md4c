import sys, os
import platform

from . import types
from . import binds
from . import flags
from . import helpers


__all__ = ('load', 'Main')


lib = None


def load(path = None):

    """
    Load pre-build or custom libraries.

    :param str path:
        Location of the dll or dylib.

    .. note::

        Only ``Dawin`` systems are supported out of the box.

        Follow the project's `instructions <https://github.com/mity/md4c/wiki/Building-MD4C>`_ to build your own.
    """

    global lib

    if lib:
        return

    if not path:
        directory = os.path.dirname(__file__)
        directory = os.path.join(directory, 'bin')
        system = platform.system()
        for name in os.listdir(directory):
            (root, ext) = os.path.splitext(name)
            if root == system:
                break
        else:
            raise FileNotFoundError(f'Missing lib for "{system}" system')
        path = os.path.join(directory, name)

    lib = binds.load(path)


class Main:

    """
    Class for interacting with the parser.

    The ``options`` param can be ``flags`` and callbacks.

    Valid callbacks are ``(enter/leave)_(block/span)`` and ``text``.

    Flags are used to (de)activate built-in derivates and extensions.
    """

    __slots__ = ('_store', '_encoding')

    _version = 0

    def __init__(self, encoding = None, **options):

        load()

        self._store = binds.create(
            **options,
            api_version = self._version
        )

        self._encoding = encoding or sys.getdefaultencoding()

    @property
    def encoding(self):

        return self._encoding

    def parse(self, value):

        """
        Parse ``value`` with callbacks.
        """

        size = len(value)

        value = value.encode(self._encoding)

        return helpers.c_call(lib.md_parse, value, size, self._store, 0)
