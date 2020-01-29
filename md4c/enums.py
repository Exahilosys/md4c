import functools

from . import abc


__all__ = ('Block', 'Span', 'Text', 'Align')


Block = abc.Enum(
    'Block',
    'doc quote ul ol li hr h code html p table thead tbody tr th td',
    start = 0
)


Span = abc.Enum(
    'Span',
    'em strong a img code del_ latex_math latex_math_display wiki_link u',
    start = 0
)


Text = abc.Enum(
    'Text',
    'normal nullchar br soft_br entity code html latex_math',
    start = 0
)


Align = abc.Enum(
    'Align',
    'default left center right',
    start = 0
)
