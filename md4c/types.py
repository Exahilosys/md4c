import ctypes


__all__ = ('char', 'char_p', 'size', 'offset', 'enum', 'void', 'ires', 'vres')


char = ctypes.c_char


char_p = ctypes.c_char_p


size = ctypes.c_uint


offset = ctypes.c_uint


enum = ctypes.c_uint


void = ctypes.c_void_p


ires = ctypes.c_int


vres = void
