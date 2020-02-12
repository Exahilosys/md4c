import abc
import shutil

from . import flags
from . import clients
from . import details


__all__ = ('Base', 'Html', 'Ascii')


class Base(abc.ABC):

    """
    Source for all parsers.

    For custom parsers, overwrite :meth:`_leave`, :meth:`_track`, and
    :meth:`_get`. Create a ``_parse_(tag)`` method for every handled tag.
    All valid tags can be found in :class:`~.enums.Block` and
    :class:`~.enums.Span` with trailing underscores stripped.

    Flags: ``strike_through`` | ``underline``.
    """

    __slots__ = ('_client',)

    flags = flags.Spec.strike_through | flags.Spec.underline

    def __init__(self, flags = 0):

        for cls in self.__class__.__mro__:

            if not issubclass(cls, Base):

                continue

            flags |= cls.flags

        self._client = clients.Main(
            flags = flags,
            enter_block = self._enter,
            leave_block = self._leave,
            enter_span = self._enter,
            leave_span = self._leave,
            text = self._track
        )

    def _enter(self, type, info):

        name = type.name.rstrip('_')

        name = f'_parse_{name}'

        func = getattr(self, name, None)

        if not func:

            return

        func(info)

    @abc.abstractmethod
    def _track(self, type, data):

        """
        Simple text will be directed here.
        """

    @abc.abstractmethod
    def _leave(self, type, info):

        """
        Exiting tags will triger this.
        """

    @abc.abstractmethod
    def _get(self):

        """
        Should return a single :class:`str` value as the final result.
        """

    def get(self, value):

        """
        Parse the value and get the result.
        """

        self._client.parse(value)

        value = self._get()

        return value


try:

    import bs4

except ImportError:

    bs4 = None


class Html(Base):

    """
    Converts to html.

    Flags: ``tables``.

    .. warning::

        Only works with
        `bs4 <https://www.crummy.com/software/BeautifulSoup/bs4/doc>`_
        installed.
    """

    flags = flags.Spec.tables

    __slots__ = ('_tags', '_soup')

    def __init__(self, **opts):

        if not bs4:

            raise ImportError('mising "bs4" module')

        super().__init__(**opts)

        soup = bs4.BeautifulSoup(features = 'html.parser')

        self._tags = (self._soup,) = [soup]

    def _get(self):

        data = str(self._soup)

        self._soup.clear()

        return data

    def _add(self, data):

        self._tags[-1].append(data)

    def _track(self, type, data):

        self._add(data)

    def _fin(self):

        data = self._tags.pop()

        self._add(data)

    def _leave(self, type, info):

        self._fin()

    def _new(self, name, info = {}):

        value = self._soup.new_tag(name, **info)

        empty = value.is_empty_element

        (self._add if empty else self._tags.append)(value)

        return value

    def _parse_doc(self, info):

        name = 'body'

        self._new(name)

    def _parse_quote(self, info):

        name = 'blockquote'

        self._new(name)

    def _parse_ul(self, info):

        name = 'ul'

        self._new(name)

    def _parse_ol(self, info):

        name = 'ol'

        self._new(name, start = info.start)

    def _parse_li(self, info):

        name = 'li'

        self._new(name)

    def _parse_hr(self, info):

        name = 'hr'

        self._new(name)

    def _parse_h(self, info):

        name = f'h{info.level}'

        self._new(name)

    def _b_parse_code(self, info):

        name = 'pre'

        self._new(name)

        attrs = {}

        if info.lang:

            attrs['class'] = f'lang-{info.lang}'

        name = 'code'

        self._new(name, info = attrs)

        self._fin()

    def _s_parse_code(self, info):

        name = 'code'

        self._new(name)

    def _parse_code(self, info):

        (self._b_parse_code if info else self._s_parse_code)(info)

    def _parse_html(self, info):

        self._add(info)

    def _parse_p(self, info):

        name = 'p'

        self._new(name)

    def _parse_table(self, info):

        name = 'table'

        self._new(name)

    def _parse_tbody(self, info):

        name = 'tbody'

        self._new(name)

    def _parse_tr(self, info):

        name = 'tr'

        self._new(name)

    def _parse_th(self, info):

        name = 'th'

        self._new(name)

    def _parse_td(self, info):

        name = 'td'

        self._new(name)

    def _parse_em(self, info):

        name = 'em'

        self._new(name)

    def _parse_strong(self, info):

        name = 'strong'

        self._new(name)

    def _parse_a(self, info):

        attrs = {'href': info.href}

        name = 'a'

        self._new(name, info = attrs)

    def _parse_img(self, info):

        attrs = {'src': info.src}

        name = 'img'

        self._new(name, info = attrs)

    def _parse_del(self, info):

        name = 'del'

        self._new(name)

    def _parse_u(self, info):

        name = 'u'

        self._new(name)


try:

    import sty

except ImportError:

    sty = None


class Ascii(Base):

    """
    Converts to ascii escape sequences.

    Flags: ``no_html``.

    .. warning::

        Only works with `sty <https://sty.mewo.dev>`_ installed.
    """

    _empty = ''

    flags = flags.Spec.no_html

    def __init__(self, **opts):

        if not sty:

            raise ImportError('missing "sty" module')

        super().__init__(**opts)

        self._buffer = []

        self._closes = []

        self._listing = []

    def _get(self):

        zeros = (0,) * len(self._buffer)

        data = ''.join(map(self._buffer.pop, zeros))

        return data.lstrip().lstrip('\n')

    def _add(self, data):

        self._buffer.append(data)

    def _track(self, type, data):

        self._add(data)

    def _fin(self):

        data = self._closes.pop()

        self._add(data)

    def _leave(self, type, info):

        self._fin()

    def _new(self, open, close = None):

        self._buffer.append(open)

        if close is None:

            return

        self._closes.append(close)

    def _nil(self, close):

        open = self._empty

        close = open if close else None

        self._new(open, close)

    def _parse_doc(self, info):

        self._nil(1)

    def _parse_quote(self, info):

        open = sty.ef.inverse

        close = sty.rs.inverse

        self._new(open, close)

    def _parse_ul(self, info):

        self._listing.append(info)

        self._nil(1)

    def _parse_ol(self, info):

        self._listing.append(info)

        self._nil(1)

    def _fetch_li_mark_ul(self, info):

        value = info.mark

        return value

    def _fetch_li_mark_ol(self, info):

        value = f'{info.start}{mark_delimiter}'

        info.start += 1

        return value

    def _parse_li(self, info):

        level = len(self._listing) - 1

        next = ' '

        push = next * 2 * level

        l_info = self._listing[level]

        name = l_info.__class__.__name__.lower()

        name = f'_fetch_li_mark_{name}'

        mark = getattr(self, name)(l_info)

        mark = '-'

        open = f'\n{push}{mark}{next}'

        close = self._empty

        self._new(open, close)

    def _parse_hr(self, info):

        (width, height) = shutil.get_terminal_size()

        open = width * '-'

        self._new(open)

    def _parse_h(self, info):

        open = '\n# '

        close = ' #\n'

        self._new(open, close)

    def _parse_code(self, info):

        open = sty.ef.inverse

        close = sty.rs.inverse

        self._new(open, close)

    def _parse_p(self, info):

        self._nil(1)

    def _parse_em(self, info):

        open = sty.ef.italic

        close = sty.rs.italic

        self._new(open, close)

    def _parse_strong(self, info):

        open = sty.ef.bold

        close = sty.rs.bold_dim

        self._new(open, close)

    def _parse_a(self, info):

        self._nil(1)

    def _parse_img(self, info):

        open = f'\n{info.src}\n'

        self._new(open)

    def _parse_del(self, info):

        open = sty.ef.strike

        close = sty.rs.strike

        self._new(open, close)

    def _parse_u(self, info):

        self._new(sty.ef.underl, sty.rs.underl)
