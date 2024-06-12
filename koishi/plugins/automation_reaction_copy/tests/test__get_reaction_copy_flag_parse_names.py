import vampytest

from ..constants import MASK_PARSE_NAME_UNICODE, MASK_PARSE_TOPIC_CUSTOM, MASK_PARSE_TOPIC_UNICODE
from ..flag_naming import get_reaction_copy_flag_parse_names


def _iter_options():
    yield 0, 'none in name, none in topic'
    yield (
        MASK_PARSE_NAME_UNICODE | MASK_PARSE_TOPIC_CUSTOM | MASK_PARSE_TOPIC_UNICODE,
        'unicode in name, all in topic',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_reaction_copy_flag_parse_names(flags):
    """
    Tests whether ``get_reaction_copy_flag_parse_names`` works as intended.
    
    Parameters
    ----------
    flags : `int`
        Bitwise flags to determine from where and what kind of emojis should we collect.
    
    Returns
    -------
    output : `str`
    """
    output = get_reaction_copy_flag_parse_names(flags)
    vampytest.assert_instance(output, str)
    return output
