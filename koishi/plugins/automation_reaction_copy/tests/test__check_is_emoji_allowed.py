import vampytest
from hata import BUILTIN_EMOJIS, Emoji

from ..constants import MASK_PARSE_NAME_UNICODE, MASK_PARSE_TOPIC_CUSTOM, MASK_PARSE_TOPIC_UNICODE
from ..events import check_is_emoji_allowed


def _iter_options():
    emoji_0 = BUILTIN_EMOJIS['black_heart']
    emoji_1 = Emoji.precreate(202406120021)
    
    yield emoji_0, MASK_PARSE_NAME_UNICODE, True
    yield emoji_0, MASK_PARSE_TOPIC_CUSTOM, False
    yield emoji_0, MASK_PARSE_TOPIC_UNICODE, True

    yield emoji_1, MASK_PARSE_NAME_UNICODE, False
    yield emoji_1, MASK_PARSE_TOPIC_CUSTOM, True
    yield emoji_1, MASK_PARSE_TOPIC_UNICODE, False
    
    yield emoji_0, 0, False
    yield emoji_1, 0, False
    
    yield emoji_0, MASK_PARSE_NAME_UNICODE | MASK_PARSE_TOPIC_CUSTOM | MASK_PARSE_TOPIC_UNICODE, True
    yield emoji_1, MASK_PARSE_NAME_UNICODE | MASK_PARSE_TOPIC_CUSTOM | MASK_PARSE_TOPIC_UNICODE, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__check_is_emoji_allowed(emoji, flags):
    """
    Tests whether ``check_is_emoji_allowed`` works as intended.
    
    Parameters
    ----------
    emoji : ``Emoji``
        The emoji to check for.
    flags : `int`
        Bitwise flags to determine from where and what kind of emojis should we collect.
    
    Returns
    -------
    output : `bool`
    """
    output = check_is_emoji_allowed(emoji, flags)
    vampytest.assert_instance(output, bool)
    return output
