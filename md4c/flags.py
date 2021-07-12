
from . import abc


__all__ = ('Spec', 'Dialect')


class Spec(abc.Flag):

    collapse_whitespace         = 0x0001
    permissive_at_xheaders      = 0x0002
    permissive_url_autolinks    = 0x0004
    permissive_email_autolinks  = 0x0008
    no_indented_code_blocks     = 0x0010
    no_html_blocks              = 0x0020
    no_html_spans               = 0x0040
    tables                      = 0x0100
    strike_through              = 0x0200
    permissive_www_autolinks    = 0x0400
    task_lists                  = 0x0800
    latex_math_spans            = 0x1000
    wiki_links                  = 0x2000
    underline                   = 0x4000
    permissive_autolinks        = permissive_email_autolinks | permissive_url_autolinks | permissive_www_autolinks
    no_html                     = no_html_blocks | no_html_spans


class Dialect(abc.Flag):

    commonmark  = 0
    github      = Spec.permissive_autolinks | Spec.tables | Spec.strike_through | Spec.task_lists
