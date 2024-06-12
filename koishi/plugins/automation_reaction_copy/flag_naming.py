__all__ = ('get_reaction_copy_flag_parse_names',)

from .constants import MASK_PARSE_NAME_UNICODE, MASK_PARSE_TOPIC_CUSTOM, MASK_PARSE_TOPIC_UNICODE


KIND_NAMES = {
    0b00 : 'none',
    0b01 : 'custom',
    0b10 : 'unicode',
    0b11 : 'all',
}


def get_kind_name(unicode, custom):
    """
    Gets kind name for the given unicode & custom combination.
    
    Parameters
    ----------
    unicode : `bool`
        Whether unicode emoji parsing is allowed.
    custom : `bool`
        Whether custom emoji parsing is allowed.
    
    Returns
    -------
    name : `str`
    """
    return KIND_NAMES[unicode << 1 | custom]


def get_reaction_copy_flag_parse_names(flags):
    """
    Gets the parse flags' names.
    
    Parameters
    ----------
    flags : `int`
        Bitwise flags to determine from where and what kind of emojis should we collect.
    
    Returns
    -------
    names : `str`
    """
    name_kind_name = get_kind_name(
        True if (flags & MASK_PARSE_NAME_UNICODE) else False,
        False,
    )
    
    topic_kind_name = get_kind_name(
        True if (flags & MASK_PARSE_TOPIC_UNICODE) else False,
        True if (flags & MASK_PARSE_TOPIC_CUSTOM) else False,
    )
    
    return f'{name_kind_name!s} in name, {topic_kind_name!s} in topic'
