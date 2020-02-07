import os
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

    Valid callbacks are ``(enter/leave)_(block/span)`` and ``text``.

    Flags are used to (de)activate built-in derivates and extensions.
    """

    __slots__ = ('_store',)

    _version = 0

    def __init__(self, flags = 0, **callbacks):

        load()

        self._store = binds.create(
            **callbacks,
            flags = flags,
            api_version = self._version)

    def parse(self, value):

        """
        Parse ``value`` with callbacks.
        """

        size = len(value)

        value = value.encode()

        return helpers.c_call(lib.md_parse, value, size, self._store, 0)
